from rest_framework import renderers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from ..utils.utils import AuthorNotFound, AuthenticationFailure

from ..models.author import (
    Author,
    CachedAuthor,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest
)

from ..serializers.author import (
    AuthorSerializer,
    CachedAuthorSerializer,
    RetrieveFollowersSerializer,
    RetrieveFriendsSerializer,
    BaseRetrieveFollowersSerializer,
    BaseRetrieveFriendsSerializer,
    BaseRetrieveFollowingSerializer,
    FriendRequestSerializer
)

class BaseRelationsMixin(object):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    lookup_url_kwarg = "id"


class FollowerViewSet(BaseRelationsMixin, viewsets.ViewSet):
    serializer_class = BaseRetrieveFollowingSerializer

    # GET followers/:pk (Returns a list of who you are following)
    # GET followers/:author_pk/follow/:pk (This follows the pk)
    def retrieve(self, request, pk=None, author_pk=None):
        """
        Creating a following/follower relationship between authors

        Takes:
            pk: id of the person to be followed
            author_pk: id of the person that will follow

        If pk is none then we are retrieving the followers list
        """
        # Following the pk author
        if author_pk:
            author = get_object_or_404(self.queryset, id=author_pk)

            # Can handle this in a permission
            if request.user != author.user:
                raise AuthenticationFailure

            try:
                # Who we are following
                following = Author.objects.get(id=pk)
                following.add_follower(author)
                author.add_following(following)
            except:
                # Person we are following is on foreign node
                raise AuthorNotFound

            serializer = self.serializer_class(author)
        else:
            author = get_object_or_404(self.queryset, id=pk)

        serializer = self.serializer_class(author)
        return Response(serializer.data)

    def destroy(self, request, pk=None, author_pk=None):
        """
        Deleting a following/follower relationship between authors.
        This will also delete a friendship if it exists.

        Takes:
            pk: id of the person to be unfollowed
            author_pk: id of the person that is unfollowing.
        """
        author = get_object_or_404(self.queryset, id=author_pk)

        # Can handle this in a permission
        if request.user != author.user:
            raise AuthenticationFailure

        try:
            unfollowing = Author.objects.get(id=pk)
            unfollowing.remove_follower(author)
            author.remove_following(unfollowing)
        except:
            # Person we are unfollowing is on foreign node
            raise AuthorNotFound

        serializer = self.serializer_class(author)
        return Response(serializer.data)


class CreateFriendRequest(generics.CreateAPIView):
    """
    Given a json request parameter body, create the approriate
    friend/follower relationship.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    serializer_class = FriendRequestSerializer

    # TODO Lock this down. People can spoof identity and create friend requests

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # TODO. The action was successful
        # We can optionally return the author's friends list in responses
        # currently, a 201 Created and the given data are returned
        # TODO. Working, but response could be more descriptive.

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetFriends(BaseRelationsMixin, generics.RetrieveAPIView):
    """
    Queries the database with an author id and a friend id.

    Possible Exceptions:
        404: Author id does not exist
    """
    serializer_class = RetrieveFriendsSerializer
    queryset = Author.objects.all()
    lookup_url_kwarg = "aid"

    def get_queryset(self):
        return self.queryset.filter(id = self.kwargs.get(self.lookup_url_kwarg))

    # Alter the response to fit request before returning
    def retrieve(self, request, *arg, **kwargs):
        """Gets list response from super class and then alter to fit query"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Alter the data to match API specifications
        _ret = serializer.data
        _ret['query'] = 'friends'

        # Return only friends that were queried for. Probably can do this with the ORM
        _ret['authors'] = [a for a in _ret['friends'] if a == self.kwargs.get('fid')]
        # Insert the originating author to the friends list (friends with self)
        _ret['authors'].insert(0, self.kwargs.get(self.lookup_url_kwarg))

        if len(_ret['authors']) > 1:
            _ret['friends'] = 'YES'
        else:
            _ret['friends'] = "NO"

        return Response(_ret)
