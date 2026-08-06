def article_to_dict(article, *, include_content=True, include_analysis=False):
    data = {
        "id": str(article.id),
        "title": article.title,
        "tags": article.tags or [],
        "author": str(article.author.id),
    }
    if include_content:
        data["content"] = article.content
        data["created_at"] = article.created_at
        data["is_public"] = article.is_public
    if include_analysis and article.analysis:
        data["analysis"] = article.analysis
    return data