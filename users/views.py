from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
)
from users.models import User
from users.tokens import get_tokens_for_user
from tasks.tasks import send_welcome_email


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: UserProfileSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User(
            email=serializer.validated_data["email"],
            name=serializer.validated_data["name"],
        )
        user.set_password(serializer.validated_data["password"])
        user.save()

        send_welcome_email.delay(str(user.id))

        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects(email=email).first()
        if not user or not user.check_password(password):
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserProfileSerializer})
    def get(self, request):
        user = request.user
        return Response(
            {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
            },
            status=status.HTTP_200_OK,
        )