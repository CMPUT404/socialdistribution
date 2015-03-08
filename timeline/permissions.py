from rest_framework import permissions
from django.contrib.auth.models import User
from author.models import FriendRelationship


def isAuthor(request, obj):
    return obj.user.username == str(request.user)

def isPublic(request, obj):
    # if obj.acl["permissions"] == 200:
    return True

def isFriend(request, obj):
    # if obj.acl["permissions"] == 300:
    relationships = FriendRelationship.objects.filter(friendor__username = str(obj.user.username))
    for relationship in relationships:
        if (str(request.user) == relationship.friend.username):
            return True
    return False

def isFriendOnSameHost(request, obj):
    # TODO Add the actual check
    return True

def isFoF(request, obj):
    # if obj.acl["permissions"] == 302:
    f_relationships = FriendRelationship.objects.filter(friendor__username = str(obj.user.username))
    for relationship in f_relationships:
        if (str(request.user) == relationship.friend.username):
            return True
        fof_relationships = FriendRelationship.objects.filter(friendor__username = str(relationship.friend.username))
        for relationship in fof_relationships:
            if (str(request.user) == relationship.friend.username):
                return True
    return False

def isPrivateList(request, obj):
    # if obj.acl["permissions"] == 302:
    if str(request.user) in obj.acl["shared_users"]:
        return True
    return False


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return isAuthor(request, obj)


class IsFriend(permissions.BasePermission):
    """
    Custom permission to only allow friends. View Posts
    """
    def has_object_permission(self, request, view, obj):
        if isAuthor(request, obj):
            return True
        # we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in (permissions.SAFE_METHODS) :
            return isFriend(request, obj)


class Custom(permissions.BasePermission):
    """
    Custom permission to encompass weird edge cases
    """
    def has_object_permission(self, request, view, obj):
        if isAuthor(request, obj):
            return True

        switch = {
            100: isAuthor,
            200: isPublic,
            300: isFriend,
            301: isFriendOnSameHost,
            302: isFoF,
            500: isPrivateList,
        }

        return switch[obj.acl.permission](request, obj)
        #return (isPublic(request, obj) or isAuthor(request, obj) or isFriend(request, obj) or isFoF(request, obj))
