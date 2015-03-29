from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from mimetypes import guess_type
from ..renderers.image import ImageRenderer
from ..models.author import Author
from ..models.content import Post
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.renderers import JSONRenderer
import os

def get_img_path(img_id):
    mimetype = guess_type(img_id)[0]
    cur_dir = os.path.dirname(__file__)
    return ('{0}/../../{1}'.format(cur_dir, img_id), mimetype)

# GET /author/:authorid/image
class AuthorImage(ListAPIView):
    """
    Returns an image.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ImageRenderer, JSONRenderer, )

    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('aid', None)
        img_id = str(Author.objects.get(id=author_id).image)
        path, mimetype = get_img_path(img_id)
        try:
            f = open(path, 'rb')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(f, content_type=mimetype)

# GET /post/:postid/image
class PostImage(ListAPIView):
    """
    Returns an image.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ImageRenderer, )

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('postid', None)
        img_id = str(Post.objects.get(guid=post_id).image)
        path, mimetype = get_img_path(img_id)
        try:
            f = open(path, 'rb')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(f, content_type=mimetype)