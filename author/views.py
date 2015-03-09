import json
from backend.utils import UsernameNotFound
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
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

from author.serializers import AuthorSerializer

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

# GET /author/:username
class GetUserDetails(APIView):
    """
    Retrieve user details, given a valid username.

    JSON Response
    {
        user:{username:"", email:"", first_name:"", last_name:""},
        github_username:"",
        bio:"",
        server:""
    }
    """

    # TODO complete authorization permissions
    # Can anyone authenticated user access profile, or must be marked public?
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_user(kwargs['username'])

        if user:
            details = UserDetails.objects.get(user = user)
            serializer = AuthorSerializer(details)

            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            raise UsernameNotFound()

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
        user = get_user(kwargs['username'])
        if user:
            # Retrieve only the usernames of the followers for a given user
            followers = FollowerRelationship.objects.filter(followee = user)\
                .values('follower__username')

            relations = create_relationship_list(followers, 'follower__username')
            return Response({'followee':user.username, 'followers':relations})
        else:
            raise UsernameNotFound()

    def post(self, request, username, format=None):
        followee = get_user(username)
        new_follower = User.objects.get(username=request.POST.get('follower', ""))
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
            return Response({"friendor":new_follower.username, "friend":followee.username}, status=status.HTTP_201_CREATED)

        # otherwise create new follower relationship
        FollowerRelationship.objects.create(follower=new_follower, followee=followee)
        return Response({"follower":new_follower.username, "followee":followee.username}, status=status.HTTP_201_CREATED)

    def delete(self, request, username, format=None):
        # unfollow
        followee = get_user(username)
        formattted_request = str(request.body).strip("'<>()[]\"` ").replace('\'', '\"')
        new_unfollower = json.loads(formattted_request)['follower']
        new_unfollower = User.objects.get(username=new_unfollower)

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
