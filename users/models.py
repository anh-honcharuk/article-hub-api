from mongoengine import Document
from mongoengine.fields import EmailField, StringField
from django.contrib.auth.hashers import make_password, check_password


class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True)

    meta = {
        "collection": "users"
    }

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False