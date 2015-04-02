from django.core.files.base import ContentFile
from rest_framework import serializers
import base64
import imghdr


class ImageSerializer(serializers.BaseSerializer):
    """
    Converts base64 encoded image to binary
    """
    def to_internal_value(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            imgstr = data.split(';base64,')[1]
            return ContentFile(base64.b64decode(imgstr))

        return None

    """
    Converts ImageField to base64 encoded image
    """
    def to_representation(self, data):
        if data:
            return 'data:image/%s;base64,%s' % (imghdr.what(data),
                                                base64.b64encode(data.read()))
        return ''
