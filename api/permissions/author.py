from rest_framework import permissions
from rest_framework import exceptions
from ..models.author import Author


class IsEnabled(permissions.BasePermission):
    """
    Custom check to only allow enabled users access to app
    """

    def has_permission(self, request, view):
        author = Author.objects.get(user__id=request.user.id)
        # if not author.enabled:
        #     raise exceptions.AuthenticationFailed('account pending approval by admin')
        #
        # return True
        return author.enabled
