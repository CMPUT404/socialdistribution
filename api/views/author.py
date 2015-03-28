from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..utils.utils import AuthorNotFound, AuthenticationFailure
from ..permissions.author import IsEnabled
from ..integrations import Integrator
from api_settings import settings

from collections import OrderedDict

from ..models.author import (
    Author,
    CachedAuthor
)
from ..serializers.author import CachedAuthorSerializer
from ..serializers.relations import (
    # RetrieveFriendsSerializer,
    BaseRetrieveFollowingSerializer,
    FriendRequestSerializer,
    APIRetrieveFriendsSerializer
)


class BaseRelationsMixin(object):
    authentication_classes = (TokenAuthentication, IsEnabled)
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
            self.call_model(author.add_friend, friend)
        """
        try:
            method(self.return_cached_author(relator))
        except:
            raise AuthorNotFound

    def get_author(self, id):
        try:
            return Author.objects.get(id=id)
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

    def remove_friend(self, author, friend):
        self.call_model(author.remove_friend, friend)

    def remove_following(self, author, following):
        self.call_model(author.remove_following, following)

    def remove_request(self, author, friend):
        self.call_model(author.remove_request, friend)

    def query_foreign_author(self, author):
        # TODO after integration
        pass


class FriendsWith(APIView):
    authentication_classes = (TokenAuthentication, IsEnabled)
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
    viewsets.ViewSet
):
    serializer_class = BaseRetrieveFollowingSerializer

    # GET author/:pk (Returns a list of who you are following)
    # GET author/:author_pk/follow/:pk (This follows the pk)
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
                print "Trying to spoof author"
                raise AuthenticationFailure

            # Who we are following
            follow = get_object_or_404(self.queryset, id=pk)
            author.follow(follow)
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

        self.remove_following(author, unfollowing)

        serializer = self.serializer_class(author)
        return Response(serializer.data)


class CreateFriendRequest(ModifyRelationsMixin, generics.CreateAPIView):
    """
    Given a json request parameter body, create the approriate
    friend/follower relationship.
    """
    authentication_classes = (TokenAuthentication, IsEnabled)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get our author and friend models
        author = self.get_author(serializer.validated_data['author']['id'])
        friend_id = serializer.validated_data["friend"]["id"]
        try:
            friend = self.get_author(friend_id)
        except:
            friend = CachedAuthor.objects.get(id=friend_id)

        requestHost = "http://%s/" % request.get_host()
        # parse any incoming api calls from other nodes
        if requestHost not in [settings.HOST, settings.FRONTEND_HOST, "http://testserver/"]:
            author.add_request(friend)

        # Otherwise, figureout how to handle the request
        else:
            # perform remote calls if necessary
            if friend.is_local() is False:
                integrator = Integrator.build_from_host(friend["host"])
                success = integrator.send_friend_request(
                    CachedAuthor(**serializer.data["author"]),
                    friend
                )

                if not success:
                    # TODO: Exception of some sort
                    pass

                author.follow(friend)
                author.add_pending(friend)

            # otherwise assume we're operating on two local authors
            else:
                # if both want to be friends, make it so
                if author.is_pending_friend(friend):
                    author.add_friend(friend)
                    friend.add_friend(author)
                else:
                    author.add_pending(friend)
                    friend.add_request(author)

        return Response(status=status.HTTP_200_OK)


class GetFriends(BaseRelationsMixin, generics.RetrieveAPIView):
    """
    Queries the database with an author id and a friend id.

    Possible Exceptions:
        404: Author id does not exist
    """
    serializer_class = APIRetrieveFriendsSerializer
    queryset = Author.objects.all()
    lookup_url_kwarg = "aid"

    def get_serializer_context(self):
        """
        Provide the serializer_class with a nested relations queryset.
        """
        author = self.get_object()
        queryset = author.friends.filter(id=self.kwargs.get("fid"))

        context = super(GetFriends, self).get_serializer_context()
        context['nested_queryset'] = queryset
        return context


class QueryAuthors(APIView):
    """
    Queries the database for all cached authors

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        cached_authors =  CachedAuthor.objects.all()
        serializer = CachedAuthorSerializer(cached_authors, many=True)
        return Response({"authors": serializer.data}, status=status.HTTP_200_OK)
