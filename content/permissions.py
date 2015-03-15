from rest_framework import permissions
from author.models import Author, FriendRelationship

def isAuthor(request, obj):
    author = Author.objects.get(user = request.user)
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
    # if obj.acl["permissions"] == 200:
    return True

def isOnSameHost(request, obj):
    # TODO Add the actual check
    return True

def isFriend(request, obj):
    # if obj.acl["permissions"] == 300:
    author = Author.objects.get(user = request.user)
    relationships = FriendRelationship.objects.filter(friendor__id = obj.author.id)

    for relationship in relationships:
        if (author.id == relationship.friend.id):
            return True
    return False

def isFriendOnSameHost(request, obj):
    # TODO Add the actual check
    return True

def isFoF(request, obj):
    # if obj.acl["permissions"] == 302:
    author = Author.objects.get(user = request.user)
    f_relationships = FriendRelationship.objects.filter(friendor__id = obj.author.id)
    for relationship in f_relationships:
        if (author.id == relationship.friend.id):
            return True
        fof_relationships = FriendRelationship.objects.filter(friendor__id = relationship.friend.id)
        for relationship in fof_relationships:
            if (author.id == relationship.friend.id):
                return True
    return False

def isPrivateList(request, obj):
    # if obj.acl["permissions"] == 302:
    author = Author.objects.get(user = request.user)

    if str(author.id) in obj.acl.shared_users:
        return True

    return False


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
        if isAuthor(request, obj):
            return True
        # we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in (permissions.SAFE_METHODS) :
        return isFriend(request, obj)


class Custom(permissions.BasePermission):
    """
    Custom permission to encompass weird edge cases
    """
    def has_object_permission(self, request, view, obj):
        switch = {
            100: isAuthor,
            200: isPublic,
            300: isFriend,
            301: isFriendOnSameHost,
            302: isFoF,
            500: isPrivateList,
        }
        # Author always has permissions
        if isAuthor(request, obj):
            return True

        # we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == "DELETE":
            return isOwner(request, obj) #Obviously not author at this point
        return switch[obj.acl.permissions](request, obj)

        #return (isPublic(request, obj) or isAuthor(request, obj) or isFriend(request, obj) or isFoF(request, obj))
