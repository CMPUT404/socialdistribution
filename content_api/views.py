# TODO: Author imported but never used
from author_api.models import Author, FriendRelationship

from models import Post, Comment
from serializers import (
    PostSerializer,
    CommentSerializer
)

# TODO: IsFriend imported but never used
from permissions import IsAuthor, Custom
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import list_route
from rest_framework.exceptions import APIException

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

class PostMixin(object):
    """
    Authentication may take one of two values:
        BasicAuthentication: An external node is accessing posts.
        TokenAuthentication: A 'home' node user is accessing posts.
    """
    authentication_classes = (BasicAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, Custom,)
    serializer_class = PostSerializer

class BasePostListRetrieval(PostMixin, generics.ListAPIView):
    """
    Returns a listing of posts.
    """
    renderer_classes = (PostsJSONRenderer,)

class PostPermissionsMixin(object):
    # For querysets that only return a single object
    def get_object(self):
        post = self.get_queryset()
        self.check_object_permissions(self.request, post)
        return post

class GetPostsByAuthor(BasePostListRetrieval):
    """
    Returns a listing of posts for the given author ID

    Takes:
        id: The uuid of an author model.
    """
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        posts = Post.objects.filter(author__id=id)
        for post in posts:
            # We still want to return posts, but only those that we have permissions
            # for
            try:
                self.check_object_permissions(self.request, post)
            except APIException:
                posts.remove(post)


        return posts


class GetSinglePostByAuthor(PostMixin, PostPermissionsMixin, generics.RetrieveAPIView):
    """
    Returns a single post given an author id and a postid

    Takes:
        postid: The uuid of a post model.
        id: The uuid of an author model.
    """
    lookup_url_kwargs = ('id', 'postid')

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwargs[0])
        postid = self.kwargs.get(self.lookup_url_kwargs[1])
        return Post.objects.get(author__id=id, guid=postid)

class PostBaseView():
    serializer_class = PostSerializer
    renderer_classes = (PostsJSONRenderer,)

class PublicPostViewSet(
    PostBaseView,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Post.objects.filter(visibility="PUBLIC")

# Does everything except /post which has different permissions
class PostViewSet(
  PostBaseView,
  mixins.CreateModelMixin,
  mixins.DestroyModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  viewsets.GenericViewSet,
  PostPermissionsMixin
):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, Custom]
    queryset = Post.objects.all()

    # For querysets that only return a single object
    def get_object(self):
        post = self.get_queryset()
        self.check_object_permissions(self.request, post)
        return post
