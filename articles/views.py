from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from mongoengine.errors import ValidationError

from articles.models import Article
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
)
from articles.utils import article_to_dict

from tasks.tasks import analyze_article


def get_article_or_404(article_id):
    try:
        return Article.objects.get(id=article_id)
    except (Article.DoesNotExist, InvalidId, ValidationError):
        return None


class ArticleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="search", type=str, required=False),
            OpenApiParameter(name="tag", type=str, required=False),
        ],
        responses={200: ArticleListSerializer(many=True)},
    )
    def get(self, request):
        user = request.user
        qs = Article.objects(Q(author=user) | Q(is_public=True))

        search = request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        tag = request.query_params.get("tag")
        if tag:
            qs = qs.filter(tags=tag)

        qs = qs.order_by("-created_at")
        data = [article_to_dict(a, include_content=False) for a in qs]
        return Response(data)

    @extend_schema(request=ArticleCreateSerializer, responses={201: ArticleDetailSerializer})
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = Article(
            title=serializer.validated_data["title"],
            content=serializer.validated_data["content"],
            tags=serializer.validated_data.get("tags", []),
            is_public=serializer.validated_data.get("is_public", True),
            author=request.user,
        )
        article.save()

        return Response(
            article_to_dict(article, include_analysis=True),
            status=status.HTTP_201_CREATED,
        )


class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: ArticleDetailSerializer})
    def get(self, request, article_id):
        article = get_article_or_404(article_id)
        if not article:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if article.author.id != user.id and not article.is_public:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(article_to_dict(article, include_analysis=True))

    @extend_schema(request=ArticleUpdateSerializer, responses={200: ArticleDetailSerializer})
    def put(self, request, article_id):
        article = get_article_or_404(article_id)
        if not article:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if article.author.id != request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for field in ("title", "content", "tags", "is_public"):
            if field in serializer.validated_data:
                setattr(article, field, serializer.validated_data[field])
        article.save()

        return Response(article_to_dict(article, include_analysis=True))

    def delete(self, request, article_id):
        article = get_article_or_404(article_id)
        if not article:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if article.author.id != request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleAnalyzeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        article = get_article_or_404(article_id)
        if not article:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if article.author.id != request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        analyze_article.delay(str(article.id))

        return Response(
            {"detail": "Analysis started."},
            status=status.HTTP_202_ACCEPTED,
        )