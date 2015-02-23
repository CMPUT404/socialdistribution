from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    """
    Post
    """
    text = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    acl = models.IntegerField(null=True)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, blank=False) # Prototyping without for now

class Comment(models.Model):
    """
    Comment
    """
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey('Post')
