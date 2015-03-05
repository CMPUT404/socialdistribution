from rest_framework import generics

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

# GET /author/:username
class GetUserDetails(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    lookup_fields = ('user')

# GET /author/friends/:username
class GetAuthorFriends(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FriendRelationship.objects.all()
    serializer_class = FriendRelationshipSerializer
    lookup_fields = ('user')

# GET /author/followers/:username
class GetAuthorFollowers(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FollowerRelationship.objects.all()
    serializer_class = FollowerRelationshipSerializer
    lookup_fields = ('user')

# GET /author/friendrequests/:username
class GetAuthorFriendRequests(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    lookup_fields = ('user')

# PUT /author/update
# TODO
