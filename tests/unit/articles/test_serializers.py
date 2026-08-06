import pytest

from articles.serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleUpdateSerializer,
)


def test_article_create_serializer_valid():
    """Test valid article creation data."""
    serializer = ArticleCreateSerializer(
        data={
            "title": "Test Article",
            "content": "Test content",
            "tags": ["python", "django"],
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["title"] == "Test Article"
    assert serializer.validated_data["tags"] == ["python", "django"]
    assert serializer.validated_data["is_public"] is True


def test_article_create_serializer_defaults():
    """Test default values for article creation."""
    serializer = ArticleCreateSerializer(
        data={
            "title": "Test Article",
            "content": "Test content",
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["tags"] == []
    assert serializer.validated_data["is_public"] is True


@pytest.mark.parametrize(
    "data",
    [
        {
            "content": "Test content",
        },
        {
            "title": "Test Article",
        },
        {
            "title": "",
            "content": "Test content",
        },
    ],
)
def test_article_create_serializer_invalid_data(data):
    """Test validation of invalid article creation data."""
    serializer = ArticleCreateSerializer(data=data)

    assert not serializer.is_valid()


def test_article_create_serializer_title_too_long():
    """Test validation when the article title exceeds the maximum length."""
    serializer = ArticleCreateSerializer(
        data={
            "title": "a" * 256,
            "content": "Test content",
        }
    )

    assert not serializer.is_valid()
    assert "title" in serializer.errors


def test_article_update_serializer_partial_data():
    """Test updating an article with partial data."""
    serializer = ArticleUpdateSerializer(
        data={
            "title": "Updated title",
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["title"] == "Updated title"


def test_article_update_serializer_empty_data():
    """Test that empty update data is valid for a partial update."""
    serializer = ArticleUpdateSerializer(data={})

    assert serializer.is_valid()


def test_article_list_serializer():
    """Test serialization of article list data."""
    data = {
        "id": "123",
        "title": "Test Article",
        "tags": ["python"],
        "author": "author@example.com",
    }

    serializer = ArticleListSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["title"] == "Test Article"


def test_article_detail_serializer():
    """Test serialization of detailed article data."""
    data = {
        "id": "123",
        "title": "Test Article",
        "content": "Test content",
        "tags": ["python"],
        "author": "author@example.com",
        "analysis": {
            "word_count": 2,
        },
        "is_public": True,
    }

    serializer = ArticleDetailSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["title"] == "Test Article"