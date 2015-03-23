from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from mimetypes import guess_extension, guess_type
from django.core.files.base import ContentFile
from rest_framework import serializers
import uuid
import base64

from rest_api.utils import AuthorNotFound

from models import (
    Author,
    CachedAuthor)

from collections import OrderedDict

class ImageSerializer(serializers.BaseSerializer):
    """
    Converts base64 encoded image to binary
    """
    def to_internal_value(self, data):
        try:
            extension =  guess_extension(guess_type(data[0:23])[0])
            filename = str(uuid.uuid4()) + extension
            return ContentFile(base64.b64decode(data[23:]), name=filename)
        except:
            return None

class PostImageSerializer(ImageSerializer):
    def to_representation(self, data):
        if data:
            return '/author/posts/images/' + data.name.split('/')[-1]
        else:
            return ''

class AuthorImageSerializer(ImageSerializer):
    def to_representation(self, data):
        if data:
            return '/author/profile/images/' + data.name.split('/')[-1]
        else:
            return ''

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
    image = AuthorImageSerializer(required = False)

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
        instance.image = validated_data.get('image', instance.image)
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
    image = AuthorImageSerializer(required = False)

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
        _author['image'] = validated_data.pop('image','')

        #TODO: set host

        user = User.objects.create_user(**validated_data)
        user.save()

        author = Author(user = user, **_author)
        author.save()

        # Upon registration we also create a CachedAuthor for relationships
        # TODO host currently defaults
        cached = CachedAuthor(id = author.id, displayname = user.username)
        cached.save()

        return author

class CompactAuthorSerializer(serializers.ModelSerializer):
    displayname = serializers.CharField(source='user.username')

    class Meta:
        model = Author
        fields = ('id', 'displayname', 'host', 'url')

# This will throw an error if duplicate id's
class CachedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CachedAuthor
        fields = ('id', 'host', 'displayname', 'url',)

# This will not throw an error if duplicate id's and istead return existing model
class DirtyCachedAuthorSerializer(serializers.Serializer):
    id = serializers.UUIDField(required = True)
    host = serializers.URLField(required = True)
    displayname = serializers.CharField(required = True)
    url = serializers.URLField(required = False)

    def to_internal_value(self, data):
        """Use the superclass to clean the data and then manually save it"""
        ret = serializers.Serializer.to_internal_value(self, data)
        self.save(ret)
        return ret

    def save(self, validated_data):
        """
        Only save the model if it does not exist already
        This is done, as foreign node CachedAuthors may not already exist.
        """
        try:
            existing = CachedAuthor.objects.get(id = validated_data['id'])
            return self.update(existing, validated_data)
        except:
            return self.create(validated_data)

    def create(self, validated_data):
        cached = CachedAuthor(**validated_data)
        cached.save()
        return cached

class BaseRetrieveFollowersSerializer(serializers.ModelSerializer):
    followers = CachedAuthorSerializer(many = True)

    class Meta:
        model = Author
        fields = ('followers',)

class BaseRetrieveFriendsSerializer(serializers.ModelSerializer):
    friends = CachedAuthorSerializer(many = True)

    class Meta:
        model = Author
        fields = ('friends',)

class RetrieveFollowersSerializer(BaseRetrieveFollowersSerializer):
    """Provideds only a list of the follower guids in the return object"""
    followers = serializers.StringRelatedField(many=True)

class RetrieveFriendsSerializer(BaseRetrieveFriendsSerializer):
    """Provides only a list of the friend guids in the return object"""
    friends = serializers.StringRelatedField(many=True)

class AuthorRelationSerializer(serializers.ModelSerializer):
    """writable serializer for followers and friends only"""
    followers = CachedAuthorSerializer(many = True)

    class Meta:
        model = Author
        fields = ('followers', 'friends')
        read_only_fields = ('user', 'id', 'host', 'bio', 'github_username', \
            'image',)

class AuthorSerializer(serializers.ModelSerializer):
    displayname = serializers.CharField(source='user.username')
    email       = serializers.EmailField(source='user.email')
    first_name  = serializers.CharField(source='user.first_name')
    last_name   = serializers.CharField(source='user.last_name')
    image       = AuthorImageSerializer(required = False)

    class Meta:
        model = Author
        fields = ('id', 'displayname', 'email', 'first_name', 'last_name', \
            'github_username', 'bio', 'host', 'url', 'image')

# Serializer for given API specs
# https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
class FriendRequestSerializer(serializers.Serializer):
    query = serializers.RegexField('(friendrequest?)', allow_blank=False)
    author = DirtyCachedAuthorSerializer()
    friend = DirtyCachedAuthorSerializer()

    def save(self):
        """
        Do not save serializer data, as it is done with the field serializers
        Do create the friendship/follower relationships if valid.
        """
        self.create(self.validated_data)
        pass

    def create(self, validated_data):
        """
        Creates the friendship if dependencies satisfied, else just follow.

        If a request is given for an author that does not exist, an exception
        message is returned along with a 404 error response.
        """
        try:
            author = Author.objects.get(id = validated_data['author']['id'])
            cached = CachedAuthor.objects.get(id = str(validated_data['friend']['id']))

            # Adding the follower, will automatically determine if friend
            # request is valid and promote the relationship.
            author.add_follower(cached)
            return None
        except:
            raise AuthorNotFound
