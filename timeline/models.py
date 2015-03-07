from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Post
    """
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True, editable = False)
    public = models.BooleanField(null = False, default = False)
    fof = models.BooleanField(null = False, default = False)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, blank=False, editable = False)

class Comment(models.Model):
    """
    Comment

    A comment's privacy is inherited from the Post public attribute
    """
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey('Post')
