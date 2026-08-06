import pytest

from users.models import User
from users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


def test_register_serializer_valid():
    """Validate registration data with correct user information."""
    serializer = RegisterSerializer(
        data={
            "email": "test@example.com",
            "name": "Test User",
            "password": "string123",
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["email"] == "test@example.com"
    assert serializer.validated_data["name"] == "Test User"


def test_register_serializer_invalid_email():
    """Reject registration data with an invalid email address."""
    serializer = RegisterSerializer(
        data={
            "email": "invalid-email",
            "name": "Test User",
            "password": "string123",
        }
    )

    assert not serializer.is_valid()
    assert "email" in serializer.errors


def test_register_serializer_short_password():
    """Reject registration data when the password is too short."""
    serializer = RegisterSerializer(
        data={
            "email": "test@example.com",
            "name": "Test User",
            "password": "123",
        }
    )

    assert not serializer.is_valid()
    assert "password" in serializer.errors


def test_register_serializer_missing_name():
    """Reject registration data when the name is missing."""
    serializer = RegisterSerializer(
        data={
            "email": "test@example.com",
            "password": "string123",
        }
    )

    assert not serializer.is_valid()
    assert "name" in serializer.errors


def test_register_serializer_duplicate_email():
    """Reject registration when the email is already registered."""
    user = User(
        email="test@example.com",
        name="Existing User",
    )
    user.set_password("string123")
    user.save()

    serializer = RegisterSerializer(
        data={
            "email": "test@example.com",
            "name": "New User",
            "password": "string123",
        }
    )

    assert not serializer.is_valid()
    assert "email" in serializer.errors


def test_login_serializer_valid():
    """Validate login data with correct credentials."""
    user = User(
        email="test@example.com",
        name="Test User",
    )
    user.set_password("string123")
    user.save()

    serializer = LoginSerializer(
        data={
            "email": "test@example.com",
            "password": "string123",
        }
    )

    assert serializer.is_valid()


def test_login_serializer_missing_password():
    """Reject login data when the password is missing."""
    serializer = LoginSerializer(
        data={
            "email": "test@example.com",
        }
    )

    assert not serializer.is_valid()
    assert "password" in serializer.errors


def test_user_profile_serializer():
    """Serialize user profile data without exposing the password."""
    user = User(
        email="test@example.com",
        name="Test User",
    )
    user.set_password("string123")
    user.save()

    serializer = UserProfileSerializer(user)

    assert serializer.data["email"] == "test@example.com"
    assert serializer.data["name"] == "Test User"
    assert "password" not in serializer.data