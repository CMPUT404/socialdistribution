from django.contrib.auth.models import User
from rest_framework import serializers
from image import ImageSerializer
from ..models.author import (
    Author,
    CachedAuthor
)

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
    def validate_displayname(self, value):
        """Check if user exists"""
        if User.objects.filter(username = value):
            raise serializers.ValidationError("Displayname already exists")
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
    url = serializers.URLField(required=False)

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

class BaseRetrieveFollowingSerializer(serializers.ModelSerializer):
    following = CachedAuthorSerializer(many = True)

    class Meta:
        model = Author
        fields = ('following',)

class RetrieveFollowersSerializer(BaseRetrieveFollowersSerializer):
    """Provideds only a list of the follower guids in the return object"""
    followers = serializers.StringRelatedField(many=True)

class RetrieveFriendsSerializer(BaseRetrieveFriendsSerializer):
    """Provides only a list of the friend guids in the return object"""
    friends = serializers.StringRelatedField(many=True)

class AuthorRelationSerializer(serializers.ModelSerializer):
    """writable serializer for followers and friends only"""
    followers = CachedAuthorSerializer(many = True)
    friends = CachedAuthorSerializer(many = True)
    following = CachedAuthorSerializer(many = True)

    class Meta:
        model = Author
        fields = ('followers', 'friends', 'following')
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
