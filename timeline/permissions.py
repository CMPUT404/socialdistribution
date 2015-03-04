from rest_framework import permissions
import author.models

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsFriend(permissions.BasePermission):
    """
    Custom permission to only allow friends. View Posts
    """
    def has_object_permission(self, request, view, obj):
        # we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in (permissions.SAFE_METHODS, 'POST') :
            # Write permissions are only allowed to the owner of the snippet.
            # Get author's friends
            # import pdb; pdb.set_trace()
            friends = FriendRelationship.Objects.filter(friend=obj.owner)
            print friends
            for friend in friends:
                if request.user == friend:
                    return True
