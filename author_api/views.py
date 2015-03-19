import json

from rest_api.utils import UserNotFound

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from models import (
    Author,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )

# TODO: FriendRequestSerializer is never used
from serializers import AuthorSerializer, FriendRequestSerializer

def create_relationship_list(queryset, lookup):
    """
    Return a list of relationships, given a queryset and lookup value
    """
    relationships = []

    for relation in queryset:
        relationships.append(relation[lookup])

    return relationships

# Keeping it DRY
def get_author(id):
    try:
        return Author.objects.get(id = id)
    except:
        return None

class GetAuthorDetails(generics.RetrieveAPIView):
    serializer_class = AuthorSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Author.objects.filter(id =
            self.kwargs.get(self.lookup_url_kwarg))

# GET /author/friends/:id
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

        author = get_author(kwargs['id'])

        if author:
            # Retrieve only the usernames of the friendors for a given friend
            friendors = FriendRelationship.objects.filter(friend = author)\
                .values('friendor__id')

            relations = create_relationship_list(friendors, 'friendor__id')
            return Response({'friend':author.id, 'friendors':relations})
        else:
            raise UserNotFound()

# GET /author/followers/:id
class GetAuthorFollowers(APIView):
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        author = get_author(kwargs['id'])
        if author:
            # Retrieve only the usernames of the followers for a given user
            followers = FollowerRelationship.objects.filter(followee = author)\
                .values('follower__id')

            relations = create_relationship_list(followers, 'follower__id')
            return Response({'followee':author.id, 'followers':relations})
        else:
            raise UserNotFound()

    def post(self, request, id, format=None):
        followee = get_author(id)
        new_follower = Author.objects.get(id=request.POST.get('follower', ""))
        if followee == None:
            return Response("Followee not found", status=status.HTTP_404_NOT_FOUND)
        if new_follower == None:
            return Response("Follower not found", status=status.HTTP_404_NOT_FOUND)
        # check if the followee also follows the new follower
        # if so create a new friend relationship and remove both foller
        # relationships
        if FollowerRelationship.objects.filter(follower=followee, followee=new_follower).count():
            FriendRelationship.objects.create(friendor=new_follower, friend=followee)
            FriendRelationship.objects.create(friendor=followee, friend=new_follower)
            FollowerRelationship.objects.get(follower=followee, followee=new_follower).delete()
            return Response({"friendor":new_follower.id, "friend":followee.id}, status=status.HTTP_201_CREATED)

        # otherwise create new follower relationship
        FollowerRelationship.objects.create(follower=new_follower, followee=followee)
        return Response({"follower":new_follower.id, "followee":followee.id}, status=status.HTTP_201_CREATED)

    def delete(self, request, id, format=None):
        # unfollow
        followee = get_author(id)
        formattted_request = str(request.body).strip("'<>()[]\"` ").replace('\'', '\"')
        new_unfollower = json.loads(formattted_request)['follower']
        new_unfollower = Author.objects.get(id=new_unfollower)

        # check whether the users are friends
        if FriendRelationship.objects.filter(friendor=followee, friend=new_unfollower).count():
            # remove the friend relationship and restore the following
            # relationship.
            FriendRelationship.objects.get(friendor=followee, friend=new_unfollower).delete()
            FriendRelationship.objects.get(friendor=new_unfollower, friend=followee).delete()
            FollowerRelationship.objects.create(follower=followee, followee=new_unfollower)
            return Response(status=status.HTTP_200_OK)

        # if the users aren't friends just remove the follower relationship
        FollowerRelationship.objects.get(follower=new_unfollower, followee=followee).delete()
        return Response(status=status.HTTP_200_OK)

# GET /author/friendrequests/:id
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
        author = get_author(kwargs['id'])

        if author:
            # Retrieve only the usernames of the requestor for a given user
            requestors = FriendRequest.objects.filter(requestee = author)\
                .values('requestor__id')

            relations = create_relationship_list(requestors, 'requestor__id')
            return Response({'requestee':author.id, 'requestors':relations})
        else:
            raise UserNotFound()
