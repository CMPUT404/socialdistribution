from rest_framework import serializers
from author import (
    CachedAuthorFieldsSerializer,
    CachedAuthorSerializer)
from ..models.author import (
    Author,
    CachedAuthor
)


class BaseRetrieveFriendsSerializer(serializers.ModelSerializer):
    friends = CachedAuthorSerializer(many=True)

    class Meta:
        model = Author
        fields = ('friends',)


class BaseRetrieveFollowingSerializer(serializers.ModelSerializer):
    following = CachedAuthorSerializer(many=True)

    class Meta:
        model = Author
        fields = ('following',)


class BaseAPIRelationSerializer(serializers.ModelSerializer):
    """
    A base serializer that follows the API specifications.

    Initiate the serializer with a nested_queryset argument in the context
    that will allow the serialization of nested friend/follow relations.

    The nested_queryset should be a queryset of friends or followers.
    """
    query = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BaseAPIRelationSerializer, self).__init__(*args, **kwargs)

        self.nested_quersyet = self.context.get('nested_queryset', None)

        if self.nested_quersyet == None:
            raise NotImplementedError(
                'Must provied a nested_querset argument in the context.')

    def get_query(self, instance):
        """
        Override this to return the query type corresponding to the API.

        For example, to return "query":"friends" or "query":"friendrequest".
        """
        raise NotImplementedError('`get_query()` must be implemented.')

    class Meta:
        model = Author
        fields = ('query',)


class APIRetrieveFriendsSerializer(BaseAPIRelationSerializer):
    """Formats a recieved friends API request in the proper format"""
    authors = serializers.SerializerMethodField(source='friends')
    friends = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('query', 'authors', 'friends')

    def get_query(self, obj):
        return "friends"

    def get_friends(self, obj):
        return "YES" if len(self.nested_quersyet) > 0 else "NO"

    def get_authors(self, obj):
        """Returns a list of authors who are friends of the instance Author"""
        friends = self.nested_quersyet

        authors = []
        # Per specs, author infront
        authors.append(str(self.instance.id))

        for f in friends:
            authors.append(str(f.id))

        return authors


# Serializer for given API specs
# https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
class FriendRequestSerializer(serializers.Serializer):
    query = serializers.RegexField('(friendrequest?)', allow_blank=False)
    author = CachedAuthorFieldsSerializer()
    friend = CachedAuthorFieldsSerializer()


class FollowRequestSerializer(serializers.Serializer):
    author = CachedAuthorFieldsSerializer()
    following = CachedAuthorFieldsSerializer()

    def save(self, validated_data):
        """
        Creates a following relationship using the created CachedAuthor
        models in the nested serializers.

        If an Author model does not exist, then the serializer will have
        already exceptioned out. The below checks are simply a further safety.
        """
        author_id = validated_data['author']['id']
        following_id = validated_data['following']['id']

        author = Author.objects.filter(id=author_id)
        following = CachedAuthor.objects.filter(id=following_id)

        if author.exists() and following.exists():
            author[0].follow(following[0])

        return author[0]
