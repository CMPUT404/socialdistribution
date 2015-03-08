from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework import status

def custom_exception_handler(exc):
    """
    Exception handler called by all raised exceptions during HTTP requests.

    Return value:
        {
            "error":"message body"
        }
    """

    # Preserve the original status_code for the new exception
    status_code = exc.status_code if exc.status_code else \
        status.HTTP_500_INTERNAL_SERVER_ERROR

    if hasattr(exc, 'detail') and not isinstance(exc.detail, unicode):
        try:
            # original error message is {'detail':[list of messages]}
            # Get values from dictionary and take first list element
            msg = exc.detail.values()[0][0]
            exc = GenericException(msg)
        except:
            exc = GenericException()

    exc.status_code = status_code
    response = exception_handler(exc)

    if response is not None:
        if response.data['detail']:
            response.data['error'] = response.data['detail']
            del response.data['detail']

    return response

class GenericException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error encountered'

class UsernameNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Username not found'

class UsernameAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username already exists'

class AuthenticationFailure(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication failed'
