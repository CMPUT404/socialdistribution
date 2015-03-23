from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from uuidfield import UUIDField

import os


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class AuthorQuerySet(models.query.QuerySet):
    def areFriends(self, authorid, friendid):
        """
        Given an author id and the friend id of who you are comparing,
        returns the author if the friendship is valid, that can be used to
        confirm a friendship.

        This will throw an exception if either guid is not valid
        """
        return self.get(id=authorid, friends__id=friendid)


class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorQuerySet(self.model, using=self._db)


class Author(models.Model):
    """
    Extends the existing Django User model as reccomended in the docs.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/
    """
    user = models.OneToOneField(User)

    id = UUIDField(auto=True, primary_key=True)
    host = models.URLField(blank=False, null=False, default=settings.HOST)

    bio = models.TextField(blank=True, null=True)
    github_username = models.CharField(max_length=40, blank=True, null=True)
    image = models.ImageField(upload_to='images/profile', blank=True, null=True)

    # Who is following the Author
    followers = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                       related_name='followers')

    # All interaction with friends should be conducted through followers
    friends = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                     related_name='friends')

    @property
    def host(self):
        return settings.HOST

    @property
    def url(self):
        return self.host + 'author/' + str(self.id)

    # Overwrites the query manager to allow custom queries from AuthorManager
    # and AuthorQueryset.
    objects = AuthorManager()

    # mixing controller logic with model logic unfortunately
    def add_follower(self, follower):
        """Create a follower from an Author/CachedAuthor model"""
        _cached = CachedAuthor.objects.get(id=follower.id)

        # Prevent duplicate entries
        if not self.followers.filter(id=follower.id):
            self.followers.add(_cached)

        # Bidirectional follow relationships become friendships
        try:
            newfriend = Author.objects.get(id=follower.id)

            # Only create a friendship if self is being followed back
            if newfriend.followers.filter(id=self.id):
                newfriend.add_friend(self)
                self.add_friend(newfriend)
        except:
            # This will fail if:
            #   1. The follower is actually foreign hosted
            # TODO
            # To determine if we can add friendship, must query foreign node
            # self.add_friend(newfriend)
            pass

    # Call add_follower instead
    def add_friend(self, follower):
        """Create a friend from an author model"""
        try:
            _cached = CachedAuthor.objects.get(id=follower.id)

            # Prevent duplicate entries
            # Cannot use a get
            if not self.friends.filter(id=follower.id):
                self.friends.add(_cached)
        except:
            pass

    def remove_follower(self, follower):
        try:
            _cached = CachedAuthor.objects.get(id=follower.id)
            self.followers.remove(_cached)
            self.remove_friend(_cached)

            # Remove from friends lists for users who friended self
            try:
                oldfriend = Author.objects.get(id=follower.id)
                oldfriend.remove_friend(self)
            except:
                # This will fail if:
                #   1. The friend is actually foreign hosted
                pass
        except:
            pass

    # Call remove_follower instead (if you remove a friend, your remove a follower)
    def remove_friend(self, friend):
        _cached = CachedAuthor.objects.get(id=friend.id)
        self.friends.remove(_cached)

    def __unicode__(self):
        return u'%s' % self.user.username


# Allows the integration of foreign and home authors into friend/follower relations
# A denormalization of sorts.
class CachedAuthor(models.Model):
    id = UUIDField(primary_key=True)
    host = models.URLField(blank=False, null=False, default=settings.HOST)
    displayname = models.CharField(max_length=40, blank=False, null=False)
    url = models.URLField(blank=False, null=False, default=settings.HOST)

    # This is used for the related string field serializer
    def __unicode__(self):
        return u'%s' % self.id


#
# These are being refactored out
#
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
