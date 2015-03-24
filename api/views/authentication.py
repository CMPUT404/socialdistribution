from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status

from ..serializers.author import (
    RegistrationSerializer,
    AuthorSerializer,
    AuthorUpdateSerializer )

from ..models.author import Author

"""
All views related to authentication/registration and update
"""

class AuthorProfile(APIView):
    """
    Takes incoming JSON, validates it and updates or returns profile
    associated with the authorization header.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = AuthorUpdateSerializer(data = request.DATA)
        if serializer.is_valid(raise_exception = True):
            user_details = Author.objects.get(user = request.user)
            instance = serializer.update(user_details, serializer.validated_data)
            details = AuthorSerializer(instance)

            return Response(details.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorRegistration(APIView):
    """
    Takes incoming JSON, validates it and builds a Author/User Model
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = RegistrationSerializer(data = request.DATA)

        if serializer.is_valid(raise_exception = True):
            author = serializer.create(serializer.validated_data)
            token, created = Token.objects.get_or_create(user=author.user)
            serializer = AuthorSerializer(author)

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

      author = Author.objects.get(user = request.user)
      serializer = AuthorSerializer(author)

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
