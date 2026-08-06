import pytest

from users.models import User
from articles.models import Article


@pytest.fixture(autouse=True)
def clear_mongo():
    User.drop_collection()
    Article.drop_collection()
    yield


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client(api_client):
    api_client.post(
        "/api/auth/register/",
        {
            "email": "test@example.com",
            "password": "string123",
            "name": "Test User",
        },
        format="json",
    )
    response = api_client.post(
        "/api/auth/login/",
        {"email": "test@example.com", "password": "string123"},
        format="json",
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client