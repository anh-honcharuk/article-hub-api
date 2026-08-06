import pytest
from rest_framework.test import APIClient

from articles.models import Article
from users.models import User


@pytest.fixture(autouse=True)
def clear_mongo():
    """Clear MongoDB collections before and after each test."""
    User.drop_collection()
    Article.drop_collection()

    yield

    User.drop_collection()
    Article.drop_collection()


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def user():
    """Create and return a test user."""
    user = User(
        email="test@example.com",
        name="Test User",
    )
    user.set_password("string123")
    user.save()

    return user


@pytest.fixture
def auth_client(api_client, user):
    """Return an API client authenticated as the test user."""
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": user.email,
            "password": "string123",
        },
        format="json",
    )

    assert response.status_code == 200

    token = response.data["access"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    return api_client