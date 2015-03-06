from backend.utils import UsernameNotFound

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from author.models import (
    UserDetails,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

from author.serializers import UserDetailSerializer

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

def create_relationship_list(queryset, lookup):
    """
    Return a list of relationships, given a queryset and lookup value
    """
    relationships = []

    for relation in queryset:
        relationships.append(relation[lookup])

    return relationships

# Keeping it DRY
def get_user(username):
    try:
        return User.objects.get(username = username)
    except:
        return None

# GET /author/friends/:username
class GetAuthorFriends(ListAPIView):
    """
    Returns a JSON object containing a friend and a list of friendors

    Expected Return JSON:
        {
            friend:"username"
            friendors: [
                "friendor_username",
                ...
            ]
        }
    """

    def list(self, request, *args, **kwargs):

        user = get_user(kwargs['username'])

        if user:
            # Retrieve only the usernames of the friendors for a given friend
            friendors = FriendRelationship.objects.filter(friend = user)\
                .values('friendor__username')

            relations = create_relationship_list(friendors, 'friendor__username')
            return Response({'friend':user.username, 'friendors':relations})
        else:
            raise UsernameNotFound()

# GET /author/followers/:username
class GetAuthorFollowers(ListAPIView):
    """
    Returns a JSON object containing a followee and a list of followers

    Expected Return JSON:
        {
            followee:"username"
            followers: [
                "follower_username",
                ...
            ]
        }
    """

    def list(self, request, *args, **kwargs):
        user = get_user(kwargs['username'])

        if user:
            # Retrieve only the usernames of the followers for a given user
            followers = FollowerRelationship.objects.filter(followee = user)\
                .values('follower__username')

            relations = create_relationship_list(followers, 'follower__username')
            return Response({'followee':user.username, 'followers':relations})
        else:
            raise UsernameNotFound()

# GET /author/friendrequests/:username
class GetAuthorFriendRequests(ListAPIView):
    """
    Returns a JSON object containing a requestee and a list of requestor

    Expected Return JSON:
        {
            requestee:"username"
            requestors: [
                "requestor_username",
                ...
            ]
        }
    """

    def list(self, request, *args, **kwargs):
        user = get_user(kwargs['username'])

        if user:
            # Retrieve only the usernames of the requestor for a given user
            requestors = FriendRequest.objects.filter(requestee = user)\
                .values('requestor__username')

            relations = create_relationship_list(requestors, 'requestor__username')
            return Response({'requestee':user.username, 'requestors':relations})
        else:
            raise UsernameNotFound()

# PUT /author/update
# TODO
