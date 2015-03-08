from rest_framework import permissions
from django.contrib.auth.models import User

from author.models import FriendRelationship

class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsFriend(permissions.BasePermission):
    """
    Custom permission to only allow friends. View Posts
    """
    def has_object_permission(self, request, view, obj):
        if obj.user.username == str(request.user):
            return True
        # we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in (permissions.SAFE_METHODS) :
            # Get author's friends
            friends = FriendRelationship.objects.filter(friendor__username = str(request.user))
            if obj.user.username in [x.friend.username for x in friends]:
                return True
