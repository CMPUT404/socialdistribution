from django.contrib.auth.models import User

from rest_framework import serializers
from author.models import (
    Author,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('user', 'uuid')

# Only to be used wuth AuthorDetailSerializer!
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

class AuthorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Author
        fields = ('user', 'uuid', 'github_username', 'bio')

class FollowerRelationshipSerializer(serializers.ModelSerializer):
    follower = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = FollowerRelationship
        fields = ('follower',)

class FriendRelationshipSerializer(serializers.ModelSerializer):
    friendor = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRelationship
        fields = ('friendor',)

class FriendRequestSerializer(serializers.ModelSerializer):
    requestor = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('requestor', )
