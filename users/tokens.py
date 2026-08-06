from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh["user_id"] = str(user.id)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }