import pytest
from rest_framework import status

from articles.models import Article
from users.models import User


def create_user(email="author@example.com", name="Author"):
    user = User(
        email=email,
        name=name,
    )
    user.set_password("string123")
    user.save()
    return user


def create_article(user, **kwargs):
    data = {
        "title": "Test Article",
        "content": "Test content",
        "tags": ["python", "django"],
        "author": user,
    }
    data.update(kwargs)

    article = Article(**data)
    article.save()
    return article


def test_create_article(auth_client):
    response = auth_client.post(
        "/api/articles/",
        {
            "title": "My first article",
            "content": "Some text",
            "tags": ["python", "django"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "My first article"
    assert response.data["content"] == "Some text"


def test_create_article_without_required_fields(auth_client):
    response = auth_client.post(
        "/api/articles/",
        {
            "title": "Only title",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_article_invalid_title(auth_client):
    response = auth_client.post(
        "/api/articles/",
        {
            "title": "a" * 256,
            "content": "Some text",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_article_unauthenticated(api_client):
    response = api_client.post(
        "/api/articles/",
        {
            "title": "Test",
            "content": "Content",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_article_list(auth_client):
    response = auth_client.post(
        "/api/articles/",
        {
            "title": "Article 1",
            "content": "Content 1",
            "tags": ["python"],
        },
        format="json",
    )

    article_id = response.data["id"]

    response = auth_client.get("/api/articles/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == article_id


def test_get_article_detail(auth_client):
    create = auth_client.post(
        "/api/articles/",
        {
            "title": "Test Article",
            "content": "Test content",
            "tags": ["python"],
        },
        format="json",
    )

    article_id = create.data["id"]

    response = auth_client.get(
        f"/api/articles/{article_id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Test Article"
    assert response.data["content"] == "Test content"


def test_get_nonexistent_article(auth_client):
    response = auth_client.get(
        "/api/articles/507f1f77bcf86cd799439011/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_article_invalid_id(auth_client):
    response = auth_client.get(
        "/api/articles/invalid-id/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_articles(auth_client):
    auth_client.post(
        "/api/articles/",
        {
            "title": "Python Tips",
            "content": "Learn Django",
            "tags": ["python"],
        },
        format="json",
    )

    auth_client.post(
        "/api/articles/",
        {
            "title": "FastAPI Guide",
            "content": "Learn FastAPI",
            "tags": ["fastapi"],
        },
        format="json",
    )

    response = auth_client.get(
        "/api/articles/?search=Python"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Python Tips"


def test_search_articles_by_content(auth_client):
    auth_client.post(
        "/api/articles/",
        {
            "title": "My Article",
            "content": "Django REST Framework",
            "tags": [],
        },
        format="json",
    )

    response = auth_client.get(
        "/api/articles/?search=Django"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_filter_articles_by_tag(auth_client):
    auth_client.post(
        "/api/articles/",
        {
            "title": "Python Article",
            "content": "Content",
            "tags": ["python"],
        },
        format="json",
    )

    auth_client.post(
        "/api/articles/",
        {
            "title": "Django Article",
            "content": "Content",
            "tags": ["django"],
        },
        format="json",
    )

    response = auth_client.get(
        "/api/articles/?tag=python"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Python Article"


def test_update_article(auth_client):
    create = auth_client.post(
        "/api/articles/",
        {
            "title": "Old title",
            "content": "Old content",
            "tags": ["python"],
        },
        format="json",
    )

    article_id = create.data["id"]

    response = auth_client.put(
        f"/api/articles/{article_id}/",
        {
            "title": "New title",
            "content": "New content",
            "tags": ["django"],
            "is_public": False,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "New title"
    assert response.data["content"] == "New content"
    assert response.data["tags"] == ["django"]
    assert response.data["is_public"] is False


def test_update_article_partial(auth_client):
    create = auth_client.post(
        "/api/articles/",
        {
            "title": "Old title",
            "content": "Old content",
        },
        format="json",
    )

    article_id = create.data["id"]

    response = auth_client.put(
        f"/api/articles/{article_id}/",
        {
            "title": "New title",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "New title"
    assert response.data["content"] == "Old content"


def test_update_other_users_article(api_client):
    owner = create_user("owner@example.com", "Owner")
    article = create_article(owner)

    other_user = create_user("other@example.com", "Other")

    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(other_user).access_token)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = api_client.put(
        f"/api/articles/{article.id}/",
        {
            "title": "Hacked",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_article(auth_client):
    create = auth_client.post(
        "/api/articles/",
        {
            "title": "To delete",
            "content": "Content",
        },
        format="json",
    )

    article_id = create.data["id"]

    response = auth_client.delete(
        f"/api/articles/{article_id}/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    detail = auth_client.get(
        f"/api/articles/{article_id}/"
    )

    assert detail.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_users_article(api_client):
    owner = create_user("owner@example.com", "Owner")
    article = create_article(owner)

    other_user = create_user("other@example.com", "Other")

    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(other_user).access_token)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = api_client.delete(
        f"/api/articles/{article.id}/"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_private_article_not_visible_to_other_user(api_client):
    owner = create_user("owner@example.com", "Owner")
    article = create_article(
        owner,
        is_public=False,
    )

    other_user = create_user("other@example.com", "Other")

    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(other_user).access_token)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = api_client.get(
        f"/api/articles/{article.id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_public_article_visible_to_other_user(api_client):
    owner = create_user("owner@example.com", "Owner")
    article = create_article(
        owner,
        is_public=True,
    )

    other_user = create_user("other@example.com", "Other")

    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(other_user).access_token)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = api_client.get(
        f"/api/articles/{article.id}/"
    )

    assert response.status_code == status.HTTP_200_OK


def test_analyze_article(auth_client):
    create = auth_client.post(
        "/api/articles/",
        {
            "title": "Test",
            "content": "Some text",
            "tags": ["python", "django"],
        },
        format="json",
    )

    article_id = create.data["id"]

    response = auth_client.post(
        f"/api/articles/{article_id}/analyze/"
    )

    assert response.status_code == status.HTTP_202_ACCEPTED


def test_analyze_other_users_article(api_client):
    owner = create_user("owner@example.com", "Owner")
    article = create_article(owner)

    other_user = create_user("other@example.com", "Other")

    from rest_framework_simplejwt.tokens import RefreshToken

    token = str(RefreshToken.for_user(other_user).access_token)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = api_client.post(
        f"/api/articles/{article.id}/analyze/"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_analyze_nonexistent_article(auth_client):
    response = auth_client.post(
        "/api/articles/507f1f77bcf86cd799439011/analyze/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND