from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from rest_framework import status

from author.models import UserDetails

from author.serializers import RegistrationSerializer

"""
All views related to authentication
"""

@api_view(['POST'])
@csrf_exempt
def AuthorRegistration(request):
    """
    Takes incoming JSON, validates it and builds a UserDetails/User Model
    """
    serializer = RegistrationSerializer(data = request.DATA)

    if serializer.is_valid(raise_exception = True):
        user_details = serializer.create(serializer.validated_data)

        return Response({'uuid':user_details.uuid}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

# Token based
class Login(APIView):
    """
    Handles a POST with a username/password and passes back a token.

    Expected incoming JSON
    {
        username:username
        password:password
    }
    """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        """Returns authentication token after validating JSON body data"""
        serializer = self.serializer_class(data = request.DATA)

        if serializer.is_valid(raise_exception = True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PasswordReset(GenericsAPIView):
#     pass
#
# class PasswordChange(GenericsAPIView):
#     pass
