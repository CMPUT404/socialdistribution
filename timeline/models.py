from django.db import models

class Post(models.Model):
    """
    Post
    """
    text = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    acl = models.IntegerField(null=True)
    image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey('author.Author', blank=False) # Prototyping without for now

class Comment(models.Model):
    """
    Comment
    """
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey('Post')
