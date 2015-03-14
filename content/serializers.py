from rest_framework import serializers

from content.models import Post, Comment, ACL

from author.models import Author
from author.serializers import CompactAuthorSerializer

import time
import datetime

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
        request = self.context.get('request', None)

        return request.build_absolute_uri(request.path_info)

class OriginSerializer(serializers.URLField):
    # Get path this post object was called from
    def get_attribute(self, post):
        request = self.context.get('request', None)

        url = request.build_absolute_uri("http://%s/author/post/%s"
            %(request.get_host(), post.guid))

        return url

class ACLSerializer(serializers.ModelSerializer):
    permissions = serializers.CharField()
    shared_users = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = ACL
        fields = ('permissions', 'shared_users')

class CommentSerializer(serializers.ModelSerializer):
    author = CompactAuthorSerializer(many=False, read_only=True)
    # pubDate = UnixDateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('guid', 'content', 'pubDate', 'author')
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
    acl = ACLSerializer(many = False)
    author = CompactAuthorSerializer(many = False, read_only = True)
    comments = CommentSerializer(read_only = True, many = True)
    # pubDate = UnixDateTimeField(read_only=True)
    source = SourceSerializer(read_only = True)
    origin = OriginSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ('guid', 'title', 'source', 'origin', 'content', 'pubDate', 'acl', 'image', 'author', 'comments')
        read_only_fields = ('guid', 'pubDate', 'comments', 'author')

    # DRF does not currently support creation of nested relations...
    def create(self, validated_data):
        request = self.context.get('request', None)

        _author = Author.objects.get(user = request.user)
        _acl = ACL.objects.create(**validated_data.pop('acl'))

        post = Post(acl = _acl, author = _author, **validated_data)
        post.save()

        return post
