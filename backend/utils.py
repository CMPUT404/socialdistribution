from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, AuthenticationFailed

def custom_exception_handler(exc, context):
    """
    Exception handler called by all raised exceptions during HTTP requests.

    Return value:
        {
            "error":"message body"
        }
    """

    if hasattr(exc, 'detail') and not isinstance(exc.detail, unicode):
        try:
            # original error message is {'detail':[list of messages]}
            # Get values from dictionary and take first list element
            msg = exc.detail.values()[0][0]
            exc = GenericException(msg)
        except:
            exc = GenericException()

    response = exception_handler(exc, context)

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
