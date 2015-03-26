from rest_framework import serializers
from ..models.content import Post, Comment
from ..models.author import Author
from author import CompactAuthorSerializer
from image import ImageSerializer
from django.conf import settings
import time

# TODO
# Date defaults to ISO-8601 as mentioned in class (but differs than example json).
# Which format to adopt?
# The calling of this serializer has been commented out.
class UnixDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        """
        Return epoch time for datetime model field.
        """
        try:
            return int(time.mktime(value.timetuple()))
        except(AttributeError, TypeError):
            return None


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
    # pubDate = UnixDateTimeField(read_only=True)

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

class PostImageSerializer(ImageSerializer):
    def to_representation(self, data):
        if data:
            return '/author/posts/images/' + data.name.split('/')[-1]
        else:
            return ''

class PostSerializer(serializers.ModelSerializer):
    author = CompactAuthorSerializer(many = False, read_only = True)
    comments = CommentSerializer(read_only = True, many = True)
    # pubDate = UnixDateTimeField(read_only=True)
    categories = serializers.ListField(required=False)
    source = SourceSerializer(read_only = True)
    origin = OriginSerializer(read_only = True)
    visibility = serializers.CharField()
    image = PostImageSerializer(required=False)

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
