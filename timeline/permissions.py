from rest_framework import permissions
from author.models import FriendRelationship

class IsOwner(permissions.BasePermission):
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
        # we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in (permissions.SAFE_METHODS) :
            # Write permissions are only allowed to the owner of the snippet.
            # Get author's friends
            # import pdb; pdb.set_trace()
            friends = FriendRelationship.objects.filter(friend=obj.user)
            print friends
            if request.user in friends:
                return True
