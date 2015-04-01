from django.core.files.base import ContentFile
from rest_framework import serializers
from mimetypes import guess_type, guess_extension
import uuid
import base64
import imghdr


class ImageSerializer(serializers.BaseSerializer):
    """
    Converts base64 encoded image to binary
    """
    def to_internal_value(self, data):
        extension = guess_extension(guess_type(data[0:23])[0])
        filename = str(uuid.uuid4()) + extension
        return ContentFile(base64.b64decode(data[23:]), name=filename)

    """
    Converts ImageField to base64 encoded image
    """
    def to_representation(self, data):
        if data:
            return 'data:image/%s;base64,%s' % (imghdr.what(data),
                                                base64.b64encode(data.read()))
        return ''
