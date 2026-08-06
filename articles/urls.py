from django.urls import path
from articles.views import ArticleListCreateView, ArticleDetailView, ArticleAnalyzeView

urlpatterns = [
    path("", ArticleListCreateView.as_view(), name="article-list-create"),
    path("<str:article_id>/analyze/", ArticleAnalyzeView.as_view(), name="article-analyze"),
    path("<str:article_id>/", ArticleDetailView.as_view(), name="article-detail"),
]