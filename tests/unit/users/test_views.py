import pytest
from rest_framework import status


@pytest.mark.parametrize(
    "data",
    [
        {
            "email": "invalid-email",
            "password": "string123",
            "name": "John Doe",
        },
        {
            "email": "user@example.com",
            "password": "123",
            "name": "John Doe",
        },
        {
            "email": "user@example.com",
            "password": "string123",
        },
    ],
)
def test_register_invalid_data(api_client, data):
    """Reject registration requests containing invalid data."""
    response = api_client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_duplicate_email(api_client):
    """Reject registration when the email is already registered."""
    data = {
        "email": "user@example.com",
        "password": "string123",
        "name": "John Doe",
    }

    first_response = api_client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    second_response = api_client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    assert first_response.status_code == status.HTTP_201_CREATED
    assert second_response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_invalid_password(api_client):
    """Reject login when the password is incorrect."""
    api_client.post(
        "/api/auth/register/",
        {
            "email": "user@example.com",
            "password": "string123",
            "name": "John Doe",
        },
        format="json",
    )

    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "user@example.com",
            "password": "wrong-password",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "Invalid email or password"


def test_login_nonexistent_user(api_client):
    """Reject login when the user does not exist."""
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "missing@example.com",
            "password": "string123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "Invalid email or password"


def test_profile_unauthenticated(api_client):
    """Reject profile requests from unauthenticated users."""
    response = api_client.get("/api/auth/profile/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_register_response(api_client):
    """Return the created user's public data after successful registration."""
    response = api_client.post(
        "/api/auth/register/",
        {
            "email": "user@example.com",
            "password": "string123",
            "name": "John Doe",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == "user@example.com"
    assert response.data["name"] == "John Doe"
    assert "id" in response.data
    assert "password" not in response.data


def test_login_response(api_client):
    """Return access and refresh tokens after successful login."""
    api_client.post(
        "/api/auth/register/",
        {
            "email": "user@example.com",
            "password": "string123",
            "name": "John Doe",
        },
        format="json",
    )

    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "user@example.com",
            "password": "string123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


def test_profile(auth_client):
    """Return the authenticated user's profile information."""
    response = auth_client.get("/api/auth/profile/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "test@example.com"
    assert response.data["name"] == "Test User"
    assert "id" in response.data