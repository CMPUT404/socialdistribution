from rest_framework import serializers
from timeline.models import Post, Comment, ACL
import time
import datetime
from copy import deepcopy
from author.serializers import CompactAuthorSerializer


class UnixDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        """
        Return epoch time for datetime model field.
        """
        try:
            return int(time.mktime(value.timetuple()))
        except(AttributeError, TypeError):
            return None

class ACLSerializer(serializers.ModelSerializer):
    permissions = serializers.CharField()
    shared_users = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = ACL
        fields = ('permissions', 'shared_users')


class CommentSerializer(serializers.ModelSerializer):
    author = CompactAuthorSerializer(many=False, read_only=True)
    # post = PostSerializer(many=False, read_only=True)
    date = UnixDateTimeField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'text', 'date', 'author')
        read_only_fields = ('date')


class PostSerializer(serializers.ModelSerializer):
    """
    Multiple posts are deserialized as a list object

    JSON Representation:
        [
            {
                user:{username:'', first_name:'', last_name:''},
                id:'',
                text:'',
                acl:{'permissions':300, 'shared_users':[]},
                date:'',
                image:''
            }
        ]

    Only for retrieval. Should not be used for insertion.
    """
    acl = ACLSerializer(many=False)
    author = CompactAuthorSerializer(many=False, read_only=True)
    date = UnixDateTimeField(read_only=True)
    # text = serializers.CharField()
    comments = CommentSerializer(read_only=True, many=True)
    # date = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ('author', 'id', 'text', 'date', 'image', 'comments', 'acl')

        # Fields that must not be set in HTTP request body
        read_only_fields = ('user' 'id', 'date', 'comments',)

    def create(self, validated_data):
        data = deepcopy(validated_data)
        acl_data = data.pop('acl', {"permissions": 300,"shared_users": []})
        acl_object = ACL.objects.create(**acl_data)
        post = Post(acl=acl_object, author=self.context['author'], **data)
        post.save()
        return post
