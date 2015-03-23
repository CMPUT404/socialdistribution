from rest_framework import renderers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListAPIView

from mimetypes import guess_type
import os

from api.utils.utils import AuthorNotFound

from models import (
    Author,
    CachedAuthor,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest
)

from serializers import (
    AuthorSerializer,
    CachedAuthorSerializer,
    RetrieveFollowersSerializer,
    RetrieveFriendsSerializer,
    BaseRetrieveFollowersSerializer,
    BaseRetrieveFriendsSerializer,
    FriendRequestSerializer )

class ImageRenderer(renderers.BaseRenderer):
    media_type = 'image/**'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data.read()

# GET /author/images/:imageid
class Images(ListAPIView):
    """
    Returns an image.
    """
    renderer_classes = (ImageRenderer, )

    # TODO: Add permissions and static IP when on server.
    def get(self, request, *args, **kwargs):
        img_id = kwargs.get('id', None)
        path_prefix = kwargs.get('path_prefix', None)
        if path_prefix not in ('profile', 'posts'):
            return Response(status=status.HTTP_404_NOT_FOUND)
        mimetype = guess_type(img_id)[0]
        cur_dir = os.path.dirname(__file__)
        path = '{0}/../images/{1}/{2}'.format(cur_dir, path_prefix, img_id)
        try:
            f = open(path, 'rb')
            return Response(f, content_type=mimetype)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BaseRelationsMixin(object):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Author.objects.all()
    lookup_url_kwarg = "id"

class BaseRetrievRelationsView(BaseRelationsMixin, generics.RetrieveAPIView):
    """Allows read only access for followers/friends"""

    def get_queryset(self):
        return self.queryset.filter(id = self.kwargs.get(self.lookup_url_kwarg))

class BaseCreateRelationsView(BaseRelationsMixin, generics.CreateAPIView):
    """Extends CreateAPIView to return a serializer instance upon saving"""

    def perform_create(self, serializer):
        return serializer.save()

class BaseDeleteRelationsView(BaseRelationsMixin, generics.DestroyAPIView):
    """Delete followers/friends"""

    def get_cached_author(self, guid):
        """Returns a CachedAuthor who will be removed from a relation"""
        try:
            return CachedAuthor.objects.get(id = guid)
        except:
            # Cached author does not exist on this server
            raise AuthorNotFound

    def remove_follower(self, author, follower):
        """
        Remove the follower and the associated friend for the given author
        Takes:
            author: Author model
            follower: CachedAuthor model
        """
        # This will remove the friendship. Follower/Friendship are dependents
        author.remove_follower(follower)


# Can potentially be moved to a viewset and router
class FollowersView(
        BaseRetrievRelationsView,
        BaseCreateRelationsView,
        BaseDeleteRelationsView):
    """Authenticated Authors can create, retrieve and delete followers"""

    def get_serializer_class(self):
        """Uses CachedAuthorSerializer when creating and deleting a relation"""
        if self.request.method == "GET":
            return BaseRetrieveFollowersSerializer
        else:
            return CachedAuthorSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a CachedAuthor and append it to the AuthorModel followers field
        """
        author = self.get_object()

        serializer = self.get_serializer(data = request.data)

        # CachedAuthor exists if following home node Author. Don't serialize
        queryset = CachedAuthor.objects.filter(id = request.data['id'])

        if not queryset:
            serializer.is_valid(raise_exception = True)
            cached_author = self.perform_create(serializer)

            author.add_follower(cached_author)
            author.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED, headers=headers)

        else:
            author.add_follower(queryset[0])
            author.save()

            # TODO send back another message ????
            return Response(status = status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Deletes the follower as well as the friend"""
        follower = self.get_cached_author(request.data['id'])
        author = self.get_object()
        self.remove_follower(author, follower)

        return Response(status = status.HTTP_204_NO_CONTENT)

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
