from rest_framework.response import Response
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import APIException
from models import Post, Comment
from serializers import PostSerializer, CommentSerializer
from permissions import IsAuthor, Custom
from author_api.models import Author
from author_api.serializers import AuthorSerializer
from renderers import PostsJSONRenderer

#
# Delete Posts and Comments
#

class BaseDeleteView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthor,)
    pass

class DeleteComment(BaseDeleteView):
    lookup_url_kwarg = "commentid"

    def get_queryset(self):
        return Comment.objects.filter(guid = self.kwargs.get(
            self.lookup_url_kwarg))

#
# Create Post and Comments
#
class CreateComment(generics.CreateAPIView):
    """
    Create a comment in the given post using postid.
    Can only create comments on posts you have permission to view.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, Custom,)
    serializer_class = CommentSerializer
    lookup_url_kwarg = "postid"

    def get_serializer_context(self):
        """
        Provide the serializer_class with Post model context needed to create a Comment
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'post': Post.objects.get(guid = self.kwargs.get(self.lookup_url_kwarg))
        }

#
# Post Retrieval for authors and timeline
#
class PostBaseView(object):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Handles permissions pertaining to posts and their various methods
class PostPermissionsMixin(object):
    """
    Authentication may take one of two values:
        BasicAuthentication: An external node is accessing posts.
        TokenAuthentication: A 'home' node user is accessing posts.
    """
    authentication_classes = (BasicAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, Custom,)

    # For querysets that only return a single object
    def get_object(self):
        post = self.get_queryset()
        self.check_object_permissions(self.request, post)
        return post


class AuthorPostViewSet(
    PostBaseView,
    viewsets.ViewSet,
    PostPermissionsMixin
):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = (Custom,)

    """
    Returns a listing of posts for the given author ID

    Takes:
        id: The uuid of an author model.
    """

    def list(self, request, author_pk=None):
        posts = self.queryset.filter(author__id=author_pk)
        for post in posts:
            # We still want to return posts, but only those that we have permissions
            # for
            try:
                self.check_object_permissions(self.request, post)
            except APIException:
                posts.remove(post)

        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data})

    def retrieve(self, request, author_pk=None, pk=None):

        # If no post id, serve author, if present, serve author's post
        if pk is None:
            author = Author.objects.get(id=author_pk)
            serializer = AuthorSerializer(author)
        else:
            post = self.queryset.get(author__id=author_pk, guid=pk)
            serializer = PostSerializer(post)

        return Response(serializer.data)

    # TIMELINE call
    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def posts(self, request):
        user = self.request.user
        # TODO: filter by author id and following ids as well
        # author = Author.objects.get(user__id=user.id)
        # followers = author.followers
        queryset = Post.objects.all().filter(author__user__id=user.id)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


# Handles all interactions with post objects
class PostViewSet(
  PostBaseView,
  PostPermissionsMixin,
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  viewsets.GenericViewSet
):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, Custom]

    # For querysets that only return a single object
    def retrieve(self, request, pk=None):
        post = self.queryset.get(guid=pk)
        self.check_object_permissions(self.request, post)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PublicPostsViewSet(
    PostBaseView,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    renderer_classes = (PostsJSONRenderer,)

    def get_queryset(self):
        return self.queryset.filter(visibility="PUBLIC")
