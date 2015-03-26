from rest_framework import renderers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from ..utils.utils import AuthorNotFound, AuthenticationFailure
from ..permissions.author import IsEnabled

from collections import OrderedDict

from ..models.author import (
    Author,
    CachedAuthor)

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


class ModifyRelationsMixin(object):
    """
    Calling conventions for interacting with the Other model to provide
    more detailed HTTP response messages for relation failures.

    Author must be an Author model.
    friend/follower/following can be either an Author or CachedAuthor model.
    """

    #
    # WIP. A lot of the controller logic within the models will be moved
    # in here such that the model is only interacting with itself and
    # preventing duplicate entries.
    #

    def call_model(self, method, relator):
        """
        Wraps the calling of a models method so that HTTP error is returned

        Pass in an Author model method and the relator to add to the method.
        eg:
            self.call_model(author.add_follower, follower)
        """
        try:
            method(self.return_cached_author(relator))
        except:
            raise RelationFailed

    def get_author(self, guid):
        try:
            return Author.objects.get(id=guid)
        except:
            raise AuthorNotFound

    def get_cached_author(self, guid):
        try:
            return CachedAuthor.objects.get(id=guid)
        except:
            raise AuthorNotFound

    def return_cached_author(self, instance):
        """Returns a CachedAuthor model given either Author or CachedAuthor"""
        if isinstance(instance, Author):
            return self.get_cached_author(instance.id)
        return instance

    def add_friend(self, author, friend):
        self.call_model(author.add_friend, friend)

    def add_follower(self, author, follower):
        self.call_model(author.add_follower, follower)

    def add_following(self, author, following):
        self.call_model(author.add_following, following)

    def remove_friend(self, author, friend):
        self.call_model(author.remove_friend, friend)

    def remove_follower(self, author, follower):
        self.call_model(author.remove_follower, follower)

    def remove_following(self, author, following):
        self.call_model(author.remove_following, following)

    def query_foreign_author(self, author):
        # TODO after integration
        pass

class FriendsWith(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(id=kwargs.get('fid'))
        potential_friends = request.data.get('authors')
        friends_list = []
        friends_query_set = Author.objects.get(id=author.id).friends.all()

        for potential_friend in potential_friends:
            if friends_query_set.filter(id=potential_friend).exists():
                friends_list.append(potential_friend)

        response_dict = OrderedDict()
        response_dict['query'] = 'friends'
        response_dict['author'] = author.id
        response_dict['friends'] = friends_list
        return Response(response_dict, status=status.HTTP_200_OK)


class FollowerViewSet(
                      BaseRelationsMixin,
                      ModifyRelationsMixin,
                      viewsets.ViewSet):
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
            except:
                # Person we are following is on foreign node
                raise AuthorNotFound

            self.add_follower(following, author)
            self.add_following(author, following)

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
        except:
            # Person we are unfollowing is on foreign node
            raise AuthorNotFound

        self.remove_follower(unfollowing, author)
        self.remove_following(author, unfollowing)

        serializer = self.serializer_class(author)
        return Response(serializer.data)


class CreateFriendRequest(generics.CreateAPIView):
    """
    Given a json request parameter body, create the approriate
    friend/follower relationship.
    """
    authentication_classes = (TokenAuthentication, IsEnabled)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    serializer_class = FriendRequestSerializer

    # TODO Lock this down. People can spoof identity and create friend requests

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        success = True

        friend = serializer.data["friend"]
        if friend["host"] is not settings.HOST:
            integrator = Integrator.build_from_host(friend["host"])
            success = integrator.send_friend_request(
                CachedAuthor(**serializer.data["author"]),
                CachedAuthor(**friend)
            )

        if success and request.get_host() is not settings.FRONTEND_HOST:
            pass
            # TODO: update friendship status to REQUESTED
            # TODO: add friend request notification to author model
        elif success:
            pass
            # TODO: update friendship status to PENDING
            # TODO: automatically add to author followers

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
