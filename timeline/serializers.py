from rest_framework import serializers
from timeline.models import Post, Comment

from author.serializers import CompactUserSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'id', 'text', 'date', 'image')

class PostsSerializer(serializers.ModelSerializer):
    """
    Multiple posts are deserialized as a list object

    JSON Representation:
        [
            {
                user:{username:'', first_name:'', last_name:''},
                id:'',
                text:'',
                date:'',
                image:''
            }
        ]

    Only for retrieval. Should not be used for insertion.
    """
    user = CompactUserSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('user', 'id', 'text', 'date', 'image')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'date')
