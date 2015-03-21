from django.db import models
from django.contrib.auth.models import User
from rest_api.utils import ListField
from uuidfield import UUIDField
from django.conf import settings
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

# Consider just making a custom User model if using UUID
# http://stackoverflow.com/questions/3641483/django-user-model-and-custom-primary-key-field
class Author(models.Model):
    """
    Extends the existing Django User model as reccomended in the docs.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/
    """
    user = models.OneToOneField(User)
    id = UUIDField(auto = True, primary_key = True)
    host = models.URLField(blank = False, null=False, default=settings.HOST)
    bio = models.TextField(blank=False, null=False)
    github_username = models.CharField(max_length=40, blank=True, null=True)
    image = models.ImageField(upload_to='images/author', blank=True, null=True)

    @property
    def host(self):
      return settings.HOST

    @property
    def url(self):
      return self.host + 'author/' + str(self.id)

    def __unicode__(self):
        return u'%s' %self.user.username

class FollowerRelationship(models.Model):
    """
    Follower
    """
    created_on = models.DateField(auto_now_add=True)
    follower = models.ForeignKey(Author, null=True, related_name='follower')
    followee = models.ForeignKey(Author, null=True, related_name='followee')

class FriendRelationship(models.Model):
    """
    Friend
    """
    created_on = models.DateField(auto_now_add=True)
    friendor = models.ForeignKey(Author, null=True, related_name='friendor')
    friend = models.ForeignKey(Author, null=True, related_name='friend')

class FriendRequest(models.Model):
    """
    Requests
    """
    created_on = models.DateField(auto_now_add=True)
    requestee = models.ForeignKey(Author, null=True, related_name='requestee')
    requestor = models.ForeignKey(Author, null=True, related_name='requestor')
