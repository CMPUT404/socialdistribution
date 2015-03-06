from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, AuthenticationFailed

checks = ['Username not found', 'Username already exists', 'Authentication failed']

def custom_exception_handler(exc):
    """
    Exception handler called by all raised exceptions during HTTP requests.

    Return value:
        {
            "error":"message body"
        }
    """

    if not isinstance(exc.detail, str):
        exc = GenericException()

    response = exception_handler(exc)

    if response is not None:
        # Uncomment to add status code in message body
        # response.data['status_code'] = response.status_code
        if response.data['detail']:
            response.data['error'] = response.data['detail']
            del response.data['detail']

    return response

class GenericException(APIException):
    status_code = 400
    default_detail = 'Error encountered'

class UsernameNotFound(APIException):
    status_code = 400
    default_detail = 'Username not found'

class UsernameAlreadyExists(APIException):
    status_code = 400
    default_detail = 'Username already exists'

class AuthenticationFailure(AuthenticationFailed):
    status_code = 401
    default_detail = 'Authentication failed'
