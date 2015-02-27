from django.contrib.auth.models import User

from rest_framework import serializers
from author.models import (
    UserDetails,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('user', 'uuid', 'github_username', 'bio', 'server')

# Only to be used with UserDetailsSerializer
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

class CompactUserSerializer(serializers.Serializer):
    """
    A compact user serializer that returns only relevant information to posts/comments
    """
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class UserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserDetails
        fields = ('user', 'uuid', 'github_username', 'bio')

class FollowerRelationshipSerializer(serializers.ModelSerializer):
    follower = UserSerializer(many=False, read_only=True)

    class Meta:
        model = FollowerRelationship
        fields = ('follower',)

class FriendRelationshipSerializer(serializers.ModelSerializer):
    friendor = UserSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRelationship
        fields = ('friendor',)

class FriendRequestSerializer(serializers.ModelSerializer):
    requestor = UserSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('requestor', )
