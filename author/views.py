from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import status, mixins, generics, serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.decorators import api_view

from author.models import (
    UserDetails,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

from author.serializers import (
    RegistrationSerializer,
    UserDetailSerializer,
    FollowerRelationshipSerializer,
    FriendRelationshipSerializer,
    FriendRequestSerializer )

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class MultipleFieldLookupMixin(object):
    """Allows the lookup of multiple fields in an url for mixins"""
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)

# GET /author/:uuid
class GetUserDetails(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    lookup_fields = ('uuid')

# GET /author/friends/:uuid
class GetAuthorFriends(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FriendRelationship.objects.all()
    serializer_class = FriendRelationshipSerializer
    lookup_fields = ('uuid')

# GET /author/followers/:uuid
class GetAuthorFollowers(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FollowerRelationship.objects.all()
    serializer_class = FollowerRelationshipSerializer
    lookup_fields = ('uuid')

# GET /author/friendrequests/:uuid
class GetAuthorFriendRequests(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    lookup_fields = ('uuid')

# PUT /author/update
# TODO

@api_view(['POST'])
@csrf_exempt
def AuthorRegistration(request):
    """
    Takes incoming JSON, validates it and builds a UserDetails/User Model
    """
    serializer = RegistrationSerializer(data = request.DATA)

    if serializer.is_valid():
        user_details = serializer.create(serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
