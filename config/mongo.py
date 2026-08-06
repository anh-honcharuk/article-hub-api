import os
import mongoengine

from dotenv import load_dotenv

load_dotenv()


def connect_mongo():
    mongoengine.connect(
        host=os.getenv("MONGODB_URI", "mongodb://localhost:27017/articlehub"),
        alias="default",
    )