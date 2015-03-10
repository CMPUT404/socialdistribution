from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import serializers

from author.models import (
    Author,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

class RegistrationSerializer(serializers.Serializer):
    """
    Validates incoming form data for user registration

    Use:
        Call .is_valid() to confirm validation.
        Call .create() to build/insert models after validation.
    """
    displayname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    bio = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    github_username = serializers.CharField()

    # Follow the same pattern to validate other fields if you desire.
    def validate_username(self, value):
        """Check if user exists"""
        if User.objects.filter(username = value):
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        """
        Returns a created Author model after saving to the database
        """
        try:
            user = User(
                email = validated_data['email'],
                username = validated_data['displayname'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()
        except:
            raise serializers.ValidationError("Error creating User")
        else:
            author = Author(
                user = user,
                github_username = validated_data['github_username'],
                bio = validated_data['bio']
            )
            author.save()

            return author

class CompactAuthorSerializer(serializers.ModelSerializer):
    displayname = serializers.CharField(source='user.username')

    class Meta:
        model = Author
        fields = ('id', 'displayname', 'host', 'url')

class AuthorSerializer(serializers.ModelSerializer):
    displayname = serializers.CharField(source='user.username')
    email       = serializers.EmailField(source='user.email')
    first_name  = serializers.CharField(source='user.first_name')
    last_name   = serializers.CharField(source='user.last_name')

    class Meta:
        model = Author
        fields = ('id', 'displayname', 'email', 'first_name', 'last_name', 'github_username', 'bio', 'host', 'url')

class CompactUserSerializer(serializers.Serializer):
    """
    A compact user serializer that returns only relevant information to posts/comments
    """
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class FollowerRelationshipSerializer(serializers.ModelSerializer):
    follower = CompactUserSerializer(many=False, read_only=True)

    class Meta:
        model = FollowerRelationship
        fields = ('follower',)

class FriendRelationshipSerializer(serializers.ModelSerializer):
    friendor = CompactUserSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRelationship
        fields = ('friendor',)

class FriendRequestSerializer(serializers.ModelSerializer):
    requestor = CompactUserSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('requestor', )
