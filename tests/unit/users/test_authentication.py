import pytest
from bson import ObjectId
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    AuthenticationFailed,
)

from users.authentication import MongoJWTAuthentication
from users.models import User


def test_get_user_without_user_id_claim():
    """Raise InvalidToken when the JWT does not contain a user ID claim."""
    authentication = MongoJWTAuthentication()

    with pytest.raises(InvalidToken):
        authentication.get_user({})


def test_get_user_user_not_found():
    """Raise AuthenticationFailed when the user does not exist."""
    authentication = MongoJWTAuthentication()

    token = {
        "user_id": str(ObjectId()),
    }

    with pytest.raises(AuthenticationFailed) as exc_info:
        authentication.get_user(token)

    assert str(exc_info.value.detail["detail"]) == "User not found"


def test_get_user_success():
    """Return the user when a valid user ID is provided in the JWT."""
    user = User(
        email="auth@test.com",
        name="Auth User",
    )
    user.set_password("password")
    user.save()

    authentication = MongoJWTAuthentication()

    token = {
        "user_id": str(user.id),
    }

    result = authentication.get_user(token)

    assert result.id == user.id
    assert result.email == "auth@test.com"