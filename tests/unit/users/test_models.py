from users.models import User


def test_create_user():
    """Create a user and verify its basic fields and password."""
    user = User(
        email="test@example.com",
        name="Test User",
    )
    user.set_password("string123")
    user.save()

    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.check_password("string123")
    assert not user.check_password("wrong-password")


def test_user_password_is_hashed():
    """Verify that the user's password is stored as a hash."""
    user = User(
        email="test@example.com",
        name="Test User",
    )
    user.set_password("string123")

    assert user.password != "string123"


def test_user_is_authenticated():
    """Verify that a user is authenticated and not anonymous."""
    user = User(
        email="test@example.com",
        name="Test User",
    )

    assert user.is_authenticated is True
    assert user.is_anonymous is False