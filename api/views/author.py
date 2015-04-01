from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..utils.utils import AuthorNotFound, NotAuthor
from ..permissions.author import IsEnabled
from ..integrations import Integrator, Aggregator
from api_settings import settings

from collections import OrderedDict

from ..models.author import (
    Author,
    CachedAuthor
)
from ..serializers.author import CachedAuthorSerializer
from ..serializers.relations import (
    BaseRetrieveFollowingSerializer,
    FriendRequestSerializer,
    FollowRequestSerializer,
    APIRetrieveFriendsSerializer
)


class BaseRelationsMixin(object):
    authentication_classes = (TokenAuthentication, IsEnabled)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    lookup_url_kwarg = "id"


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


class FollowerViewSet(BaseRelationsMixin, viewsets.ViewSet):
    serializer_class = FollowRequestSerializer
    permission_classes = (IsAuthenticated,)

    # POST author/:author_pk/follow
    # Create a follow relationship
    def create(self, request, author_pk=None):
        author = get_object_or_404(self.queryset, id=author_pk)
        self.is_author(request.user, author)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(serializer.validated_data)
            return Response(status=status.HTTP_200_OK)

    # DELETE author/:author_pk/follow/:pk
    # Delete pk CachedAuthor from author_pk following
    def destroy(self, request, pk=None, author_pk=None):
        """
        Deleting a following/follower relationship between authors.
        This will also delete a friendship if it exists.

        Takes:
            pk: id of the person to be unfollowed
            author_pk: id of the person that is unfollowing.
        """
        author = get_object_or_404(self.queryset, id=author_pk)
        self.is_author(request.user, author)

        try:
            unfollowing = Author.objects.get(id=pk)
        except:
            # Person we are unfollowing is on foreign node
            raise AuthorNotFound

        author.remove_following(unfollowing)
        return Response(status=status.HTTP_200_OK)

    def is_author(self, user, author):
        if user != author.user:
            raise NotAuthor

class CreateFriendRequest(generics.CreateAPIView):
    """
    Given a json request parameter body, create the approriate
    friend/follower relationship.
    """
    authentication_classes = (TokenAuthentication, IsEnabled)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    serializer_class = FriendRequestSerializer
    hosts = [settings.HOST, settings.FRONTEND_HOST, "http://testserver/"]

    def get_author_or_cached(self, id):
        """
        Returns an Author or CachedAuthor if author does not exist.

        It is gauranted that an CachedAuthor will be returned as it is
        created in the serialization process.
        """
        try:
            instance = Author.objects.get(id=id)
        except:
            instance = CachedAuthor.objects.get(id=id)

        return instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author_id = serializer.validated_data['author']['id']
        friend_id = serializer.validated_data["friend"]["id"]

        # get our author and friend models
        author = self.get_author_or_cached(author_id)
        friend = self.get_author_or_cached(friend_id)

        # parse any incoming api calls from other nodes
        if request.META["HTTP_ORIGIN"] not in self.hosts:
            if isinstance(friend, Author):
                friend.add_friend(author)
                return Response({"friends": friend.is_friend(author)},
                                status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        # Otherwise, figureout how to handle the request
        else:
            # perform remote calls if necessary
            if friend.is_local() is False:
                integrator = Integrator.build_from_host(friend.host)
                success = integrator.send_friend_request(
                    CachedAuthor(**serializer.data["author"]),
                    friend
                )

                if not success:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            author.add_friend(friend)

            return Response({"friends": author.is_friend(friend)},
                            status=status.HTTP_200_OK)


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
    def get(self, request, *args, **kwargs):
        cached_authors = CachedAuthor.objects.all()
        authors = CachedAuthorSerializer(cached_authors, many=True).data

        # get all available foreign authors too
        authors.extend(Aggregator.get_authors())

        return Response({"authors": authors}, status=status.HTTP_200_OK)
