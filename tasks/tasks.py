import logging

from celery import shared_task

from articles.models import Article
from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_id: str):
    user = User.objects.get(id=user_id)
    message = f"Welcome email sent to {user.email} ({user.name})"
    logger.info(message)
    return message


@shared_task
def analyze_article(article_id: str):
    article = Article.objects.get(id=article_id)

    word_count = len(article.content.split())
    unique_tags = len(set(article.tags or []))

    article.analysis = {
        "word_count": word_count,
        "unique_tags": unique_tags,
    }
    article.save()

    logger.info(
        "Article %s analyzed: word_count=%s unique_tags=%s",
        article_id,
        word_count,
        unique_tags,
    )
    return article.analysis


@shared_task
def daily_article_stats():
    count = Article.objects.count()
    logger.info("Daily article stats: total_articles=%s", count)
    return {"total_articles": count}