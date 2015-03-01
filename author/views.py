from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import mixins, generics, serializers

from author.models import (
    UserDetails,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

from author.serializers import (
    UserDetailSerializer,
    FollowerRelationshipSerializer,
    FriendRelationshipSerializer,
    FriendRequestSerializer )

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
