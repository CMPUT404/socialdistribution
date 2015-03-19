# TODO: Author imported but never used
from author_api.models import Author, FriendRelationship

from models import Post, Comment
from serializers import (
    PostSerializer,
    CommentSerializer )

# TODO: IsFriend imported but never used
from permissions import IsFriend, IsAuthor, Custom
from rest_framework import generics, mixins, viewsets, response as Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from renderers import PostsJSONRenderer

#
# Delete Posts and Comments
#

class BaseDeleteView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthor,)
    pass

class DeletePost(BaseDeleteView):
    lookup_url_kwarg = "postid"

    def get_queryset(self):
        return Post.objects.filter(guid = self.kwargs.get(
            self.lookup_url_kwarg))

class DeleteComment(BaseDeleteView):
    lookup_url_kwarg = "commentid"

    def get_queryset(self):
        return Comment.objects.filter(guid = self.kwargs.get(
            self.lookup_url_kwarg))

#
# Create Post and Comments
#

class CreatePost(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

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
        _id = self.kwargs.get(self.lookup_url_kwarg)
        posts = Post.objects.filter(author_id = _id)

        # TODO This should go in get_object(self), but its not being called
        # for some reason I can't figure out.
        # See test_get_private_post_again
        for post in posts:
            self.check_object_permissions(self.request, post)

        return posts

# TODO, The below two endpoints may be redundant. Can we get rid of one?
# class GetSinglePost(PostMixin, PostPermissionsMixin, generics.RetrieveAPIView):
class GetSinglePost(PostMixin, generics.RetrieveAPIView):
    """
    Returns a single post given only the postid

    Takes:
        postid: The uuid of a post model.
    """
    lookup_url_kwarg = 'postid'

    def get_queryset(self):

        _postid = self.kwargs.get(self.lookup_url_kwarg)
        try:
            post = Post.objects.get(guid = _postid)
        except:
            return None

        return post

class GetSinglePostByAuthor(PostMixin, PostPermissionsMixin, generics.RetrieveAPIView):
    """
    Returns a single post given an author id and a postid

    Takes:
        postid: The uuid of a post model.
        id: The uuid of an author model.
    """
    lookup_url_kwargs = ('id', 'postid')

    def get_queryset(self):
        _id = self.kwargs.get(self.lookup_url_kwargs[0])
        _postid = self.kwargs.get(self.lookup_url_kwargs[1])

        post = Post.objects.get(author_id = _id, guid = _postid)

        return post

class PostViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (BasicAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, Custom,)

    def list(self, request):
        queryset = Post.objects.get(visibility="PUBLIC")
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
