from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings

from users.models import User


class MongoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[settings.SIMPLE_JWT["USER_ID_CLAIM"]]
        except KeyError:
            raise InvalidToken("Token contains no user_id claim")

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")