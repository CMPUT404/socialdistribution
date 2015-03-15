from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import serializers

from author.models import (
    Author,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

class AuthorUpdateSerializer(serializers.Serializer):
    """
    Validates incoming form data for author profile updates

    Update passwords is done separately.
    Username cannot be updated.
    """
    email = serializers.EmailField(required = False)
    bio = serializers.CharField(required = False)
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    github_username = serializers.CharField(required = False)

    def update(self, instance, validated_data):
        """
        Updates UserDetails model with validated_data

        Takes:
            instance: An instantiated UserDetails model.
            validated_dated: Scrubed data from an HTTP request.
        """
        instance.bio = validated_data.get('bio', instance.bio)
        instance.github_username = validated_data.get('github_username', \
        instance.github_username)

        instance.save()

        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.last_name = validated_data.get('last_name', \
            instance.user.last_name)
        instance.user.first_name = validated_data.get('first_name', \
            instance.user.first_name)

        instance.user.save()

        return instance

class RegistrationSerializer(serializers.Serializer):
    """
    Validates incoming form data for user registration

    Use:
        Call .is_valid() to confirm validation.
        Call .create() to build/insert models after validation.
    """
    displayname = serializers.CharField()
    email = serializers.EmailField(required = False)
    password = serializers.CharField()
    bio = serializers.CharField(required = False)
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    github_username = serializers.CharField(required = False)

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
        # Rename the displayname key
        validated_data['username'] = validated_data.pop('displayname')

        _author = {}
        _author['github_username'] = validated_data.pop('github_username', '')
        _author['bio'] = validated_data.pop('bio', '')

        user = User.objects.create_user(**validated_data)
        user.save()

        author = Author(user = user, **_author)
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

class FollowerRelationshipSerializer(serializers.ModelSerializer):
    follower = CompactAuthorSerializer(many=False, read_only=True)

    class Meta:
        model = FollowerRelationship
        fields = ('follower',)

class FriendRelationshipSerializer(serializers.ModelSerializer):
    friendor = CompactAuthorSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRelationship
        fields = ('friendor',)

class FriendRequestSerializer(serializers.ModelSerializer):
    # requestor = CompactAuthorSerializer(many=False, read_only=True)
    requestor = serializers.StringRelatedField(many = True)

    class Meta:
        model = FriendRequest
        fields = ('requestor', )
