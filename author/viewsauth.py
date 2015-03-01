from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
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
