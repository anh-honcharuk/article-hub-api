from articles.models import Article
from users.models import User
from users.tokens import get_tokens_for_user


def test_create_user_and_article_flow():
    user = User(
        email="integration@example.com",
        name="Integration User",
    )
    user.set_password("testpass123")
    user.save()

    article = Article(
        title="Integration Article",
        content="Integration content",
        author=user,
        tags=["python", "testing"],
    )
    article.save()

    saved_article = Article.objects.get(id=article.id)

    assert saved_article.title == "Integration Article"
    assert saved_article.author.id == user.id
    assert saved_article.author.email == "integration@example.com"
    assert saved_article.tags == ["python", "testing"]


def test_article_creation_through_api(client):
    user = User(
        email="api@example.com",
        name="API User",
    )
    user.set_password("testpass123")
    user.save()

    tokens = get_tokens_for_user(user)

    response = client.post(
        "/api/articles/",
        {
            "title": "API Integration Article",
            "content": "Created through API",
            "tags": ["api", "integration"],
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {tokens['access']}",
    )

    assert response.status_code == 201

    article = Article.objects.get(title="API Integration Article")

    assert article.content == "Created through API"
    assert article.author.id == user.id
    assert article.tags == ["api", "integration"]