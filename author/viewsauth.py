from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token

from rest_framework import status

from author.serializers import RegistrationSerializer, AuthorSerializer
from author.models import UserDetails

"""
All views related to authentication
"""

class AuthorRegistration(APIView):
    """
    Takes incoming JSON, validates it and builds a UserDetails/User Model
    """

    def post(self, request):
      serializer = RegistrationSerializer(data = request.DATA)

      if serializer.is_valid(raise_exception = True):
          user_details = serializer.create(serializer.validated_data)
          token, created = Token.objects.get_or_create(user=user_details.user)
          serializer = AuthorSerializer(user_details)

          return Response({'token': token.key, 'author': serializer.data}, status=status.HTTP_201_CREATED)
      else:
          return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


# Token based
class Login(APIView):
    """
    Handles a GET with a Basic Auth and passes back a token and profile information.

    Response format:

    {
      "author": {
        "id": "1",
        "displayname": "Steve",
        "email": "steve@steves.com",
        "first_name": "steve",
        "last_name": "steve",
        "github_username": "steve",
        "bio": "It's Steve",
        "host": "http://some-host.com/",
        "url": "http://some-host.com/author/1"
        }
      "token": "steve's token hash"
    }
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
      """Returns authentication token after validating Basic Auth header"""
      token, created = Token.objects.get_or_create(user=request.user)
      login(request, request.user)

      details = UserDetails.objects.get(user = request.user)
      serializer = AuthorSerializer(details)

      return Response({'token': token.key, 'author': serializer.data})


# Token based
class Logout(APIView):
    """
    Logs out and deletes the token for a given user

    Requires HTTP Authorization header
        Authorization: Token {token here}
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Logout user with given token"""
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"success": "Successfully logged out."},
            status=status.HTTP_200_OK)
