from datetime import datetime

from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ListField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    DictField,
)

from users.models import User


class Article(Document):
    title = StringField(required=True, max_length=255)
    content = StringField(required=True)
    tags = ListField(StringField(), default=list)
    author = ReferenceField(User, required=True)
    is_public = BooleanField(default=True)
    analysis = DictField()
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "articles",
        "indexes": ["tags", "-created_at"],
    }