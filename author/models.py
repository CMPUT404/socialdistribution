from django.db import models
from django.contrib.auth.models import (
    User,
    BaseUserManager )

from uuidfield import UUIDField

# Consider just making a custom User model if using UUID
# http://stackoverflow.com/questions/3641483/django-user-model-and-custom-primary-key-field
class UserDetails(models.Model):
    """
    Extends the existing Django User model as reccomended in the docs.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/
    """
    user = models.OneToOneField(User)
    uuid = UUIDField(auto=True, editable=False)
    github_username = models.CharField(max_length=40, blank=True)
    bio = models.TextField(blank=False, null=False)
    server = models.ForeignKey('external.Server', null=True, blank=True)

class FollowerRelationship(models.Model):
    """
    Follower
    """
    created_on = models.DateField(auto_now_add=True)
    follower = models.ForeignKey(User, null=True, related_name='follower')
    followee = models.ForeignKey(User, null=True, related_name='followee')

class FriendRelationship(models.Model):
    """
    Friend
    """
    created_on = models.DateField(auto_now_add=True)
    friendor = models.ForeignKey(User, null=True, related_name='friendor')
    friend = models.ForeignKey(User, null=True, related_name='friend')

class FriendRequest(models.Model):
    """
    Requests
    """
    created_on = models.DateField(auto_now_add=True)
    requestee = models.ForeignKey(User, null=True, related_name='requestee')
    requestor = models.ForeignKey(User, null=True, related_name='requestor')
