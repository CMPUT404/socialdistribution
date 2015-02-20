from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response

from author.models import (
    Author,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )
from author.serializers import (
    AuthorSerializer,
    AuthorDetailSerializer,
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
class GetAuthorDetails(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
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
