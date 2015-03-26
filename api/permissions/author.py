from rest_framework import authentication
from rest_framework import exceptions
from ..models.author import Author


class IsEnabled(authentication.BasicAuthentication):
    """
    Custom check to only allow enabled users access to app
    """

    def authenticate_credentials(self, userid, password):
        author = Author.objects.get(user__username=userid)
        if not author.enabled:
            raise exceptions.AuthenticationFailed('account pending approval by admin')

        return super(IsEnabled, self).authenticate_credentials(userid, password)
        # return author.enabled
