from articles.models import Article
from users.models import User
from tasks.tasks import daily_article_stats, send_welcome_email


def test_welcome_email_task():
    """Send a welcome email to a newly created user."""
    user = User(email="a@b.com", name="A")
    user.set_password("pass")
    user.save()

    result = send_welcome_email(str(user.id))

    assert "Welcome email sent" in result


def test_daily_stats():
    """Return correct daily statistics for existing articles."""
    user = User(email="a@b.com", name="A")
    user.set_password("pass")
    user.save()

    article = Article(
        title="T",
        content="C",
        author=user,
        tags=["x"],
    )
    article.save()

    result = daily_article_stats()

    assert result["total_articles"] == 1