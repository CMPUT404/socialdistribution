from rest_framework import permissions
from django.conf import settings
from ..models.author import Author, FriendRelationship

def isAuthor(request, obj):
    author = Author.objects.get(user__id=request.user.id)
    return obj.author.id == author.id

def isOwner(request, obj):
    # owned by author or author of parent object
    if isAuthor(request, obj):
        return True
    try:
        if isAuthor(request, obj.post):
            return True
    except AttributeError:
        return False

def isPublic(request, obj):
    return True

def isOnSameHost(request, obj):
    # TODO Add the actual check
    return True

def isFriend(request, obj):
    # This should never fail as request.user must have Author account to be
    # authenticated
    author = Author.objects.get(user=request.user)

    try:
        # This will throw an exception if not friends
        author = Author.objects.get(user=request.user,
                                    friends__id=obj.author.id)
        return True
    except Exception as e:
        # print e
        return False


# Checks first to see if the authenticated Author is friends with the entity's
# author and if the specified author host is the same as ours
def isFriendOnSameHost(request, obj):
    return isFriend(request, obj) and obj.author.host == settings.HOST

def isFoF(request, obj):
    author = Author.objects.get(user=request.user)
    if isFriend(request, obj):
        return True
    for friend in obj.author.friends.all():
        for fof in friend.friends.all():
            if fof.id == author.id:
                return True
    return False

def isPrivateList(request, obj):
    return isAuthor(request, obj)

class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the comment or owner of the post
        if isAuthor(request, obj):
            return True
        return False


class IsFriend(permissions.BasePermission):
    """
    Custom permission to only allow friends. View Posts
    """
    def has_object_permission(self, request, view, obj):
        return isFriend(request, obj)


class Custom(permissions.BasePermission):
    """
    Custom permission to encompass weird edge cases
    """
    def has_object_permission(self, request, view, obj):
        switch = {
            "PUBLIC"  : isPublic,
            "FRIENDS" : isFriend,
            "FOAF"    : isFoF,
            "FOH"     : isFriendOnSameHost,
            "PRIVATE" : isPrivateList,
            "SERVERONLY" : isOnSameHost
        }

        # perform relationship checks only if logged in, also cool if statement bro
        if hasattr(obj, 'author') and request.auth is not None:

            # Author always has permissions
            if isAuthor(request, obj) is True:
                return True

            if request.method == "DELETE":
                return isOwner(request, obj) #Obviously not author at this point

            # finally check against visibility
            return switch[obj.visibility](request, obj)

        # Otherwise check public permissions
        elif obj.visibility in ["PUBLIC", "SERVERONLY"]:
            return isPublic(obj, request) or isOnSameHost(request, obj)

        # Default to no
        else:
            return False
