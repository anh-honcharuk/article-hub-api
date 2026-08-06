from unittest.mock import patch

from articles.models import Article
from users.models import User
from users.tokens import get_tokens_for_user


@patch("articles.views.analyze_article.delay")
def test_article_analysis_task_is_triggered(mock_delay, client):
    """Trigger the article analysis Celery task for an authenticated user."""
    user = User(
        email="analysis@example.com",
        name="Analysis User",
    )
    user.set_password("testpass123")
    user.save()

    article = Article(
        title="Article for Analysis",
        content="Content for analysis",
        author=user,
    )
    article.save()

    tokens = get_tokens_for_user(user)

    response = client.post(
        f"/api/articles/{article.id}/analyze/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {tokens['access']}",
    )

    assert response.status_code == 202
    assert response.json() == {"detail": "Analysis started."}

    mock_delay.assert_called_once_with(str(article.id))