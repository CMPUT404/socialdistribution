from rest_framework import serializers
from timeline.models import Post, Comment, ACL
import time
import datetime
from author.serializers import CompactUserSerializer


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
    class Meta:
        model = ACL
        fields = ('permissions', 'shared_users')

class PostSerializer(serializers.ModelSerializer):
    """
    Multiple posts are deserialized as a list object

    JSON Representation:
        [
            {
                user:{username:'', first_name:'', last_name:''},
                acl:{'permissions':300}
                id:'',
                text:'',
                date:'',
                image:''
            }
        ]

    Only for retrieval. Should not be used for insertion.
    """
    user = CompactUserSerializer(many=False, read_only=True)
    date = UnixDateTimeField(read_only=True)
    class Meta:
        model = Post
        fields = ('user', 'id', 'text', 'acl', 'date', 'image')

        # Fields that must not be set in HTTP request body
        read_only_fields = ('user' 'id', 'date',)


class CommentSerializer(serializers.ModelSerializer):
    date = UnixDateTimeField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'text', 'date')
        read_only_fields = ('date',)
