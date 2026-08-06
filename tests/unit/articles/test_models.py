import pytest

from articles.models import Article
from users.models import User


@pytest.fixture
def user():
    user = User(
        email="test@example.com",
        name="Test User",
    )
    user.set_password("string123")
    user.save()
    return user


def test_article_creation(user):
    article = Article(
        title="Test Article",
        content="Test content",
        author=user,
    )
    article.save()

    assert article.id is not None
    assert article.title == "Test Article"
    assert article.content == "Test content"
    assert article.author == user


def test_article_default_values(user):
    article = Article(
        title="Test Article",
        content="Test content",
        author=user,
    )
    article.save()

    assert article.tags == []
    assert article.is_public is True


def test_article_with_tags(user):
    article = Article(
        title="Python Article",
        content="Python content",
        tags=["python", "django"],
        author=user,
    )
    article.save()

    assert article.tags == ["python", "django"]


def test_article_private(user):
    article = Article(
        title="Private Article",
        content="Private content",
        author=user,
        is_public=False,
    )
    article.save()

    assert article.is_public is False


def test_article_analysis(user):
    article = Article(
        title="Test Article",
        content="Test content",
        author=user,
        analysis={
            "word_count": 2,
            "unique_tags": 2,
        },
    )
    article.save()

    assert article.analysis["word_count"] == 2
    assert article.analysis["unique_tags"] == 2


def test_article_author_is_required():
    with pytest.raises(Exception):
        Article(
            title="Test Article",
            content="Test content",
        ).validate()