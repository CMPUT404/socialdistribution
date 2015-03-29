from rest_framework.views import exception_handler
from rest_framework import status, exceptions
import ast
from django.db import models
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six

from rest_framework.response import Response

# from https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/views.py
def custom_exception_handler(exc, context):
    """
    Exception handler called by all raised exceptions during HTTP requests.

    Return value:
        {
            "error":"message body"
        }
    """

    if isinstance(exc, exceptions.APIException):
        data = {'error': exc.detail}
        return Response(data, status=exc.status_code)

    elif isinstance(exc, Http404):
        msg = ('Entity not found.')
        data = {'error': six.text_type(msg)}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = ('Permission denied.')
        data = {'error': six.text_type(msg)}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    # Marshal DRF into a standardized format
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # Note: Unhandled exceptions will raise a 500 error.
    return None

class GenericException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error encountered'

class UserNotFound(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Username not found'

class AuthorNotFound(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Author not found'

class UserAlreadyExists(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username already exists'

class AuthenticationFailure(exceptions.AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication failed'


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
