from rest_framework import serializers
from ..models.content import Post, Comment
from ..models.author import Author
from author import CompactAuthorSerializer
from image import ImageSerializer
from django.conf import settings
from api_settings import settings as api_settings


class SourceSerializer(serializers.URLField):
    # Get path this post object was called from
    def get_attribute(self, post):
        return self.context.get('source', settings.HOST)


class OriginSerializer(serializers.URLField):
    # Get path this post object was called from
    def get_attribute(self, post):
        return self.context.get('origin', settings.HOST)


class CommentSerializer(serializers.ModelSerializer):
    author = CompactAuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('guid', 'comment', 'pubDate', 'author')
        read_only_fields = ('guid', 'pubDate')

    def create(self, validated_data):
        """
        Creat a comment for a given user and post

        Requires an authenticated user and a Post model passed in as context!
        """
        request = self.context.get('request', None)

        _post = self.context.get('post', None)
        _author = Author.objects.get(user = request.user)

        comment = Comment(author = _author, post = _post, **validated_data)
        comment.save()

        return comment


class PostSerializer(serializers.ModelSerializer):
    author = CompactAuthorSerializer(many = False, read_only = True)
    comments = CommentSerializer(read_only = True, many = True)
    categories = serializers.ListField(required=False)
    source = SourceSerializer(read_only = True)
    origin = OriginSerializer(read_only = True)
    visibility = serializers.CharField()
    image = ImageSerializer(required=False)

    class Meta:
        model = Post
        fields = ('guid', 'title', 'source', 'origin', 'content', 'contentType', \
                    'pubDate', 'visibility', 'image', 'author', 'comments', 'categories')
        read_only_fields = ('guid', 'pubDate', 'comments', 'author', 'visibility')

    # DRF does not currently support creation of nested relations...
    def create(self, validated_data):
        request = self.context.get('request', None)
        _author = Author.objects.get(user = request.user)
        post = Post(author = _author, **validated_data)
        post.save()

        return post
