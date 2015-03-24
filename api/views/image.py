from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from mimetypes import guess_type
from ..renderers.image import ImageRenderer
import os

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
        path = '{0}/../../images/{1}/{2}'.format(cur_dir, path_prefix, img_id)

        try:
            f = open(path, 'rb')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(f, content_type=mimetype)
