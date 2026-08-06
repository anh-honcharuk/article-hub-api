from rest_framework import serializers


class ArticleCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
    )
    is_public = serializers.BooleanField(required=False, default=True)


class ArticleUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    content = serializers.CharField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
    )
    is_public = serializers.BooleanField(required=False)


class ArticleListSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    author = serializers.CharField()


class ArticleDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    author = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)
    analysis = serializers.DictField(required=False)
    is_public = serializers.BooleanField(required=False)