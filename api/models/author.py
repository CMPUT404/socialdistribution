from django.db import models
from django.conf import settings
from uuidfield import UUIDField
from user import APIUser
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Author(APIUser):
    """
    Extends the existing Django User model as reccomended in the docs.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/
    """
    bio = models.TextField(blank=True, null=True)
    github_username = models.CharField(max_length=40, blank=True, null=True)
    image = models.ImageField(upload_to='images/profile', blank=True, null=True)

    # Who is following the Author
    followers = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                       related_name='followers')
    # Who the author is following
    following = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                       related_name='following')
    # All interaction with friends should be conducted through followers
    friends = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                     related_name='friends')

    @property
    def url(self):
        return self.host + 'author/' + str(self.id)

    def _get_cached_author(self, instance):
        """Returns a CachedAuthor model given either Author or CachedAuthor"""
        if isinstance(instance, Author):
            return CachedAuthor.objects.get(id=instance.id)
        return instance

    def add_following(self, following):
        following = self._get_cached_author(following)
        if not self.following.filter(id=following.id):
            self.following.add(following)

    def add_follower(self, follower):
        """Create a follower from an Author/CachedAuthor model"""
        follower = self._get_cached_author(follower)

        # Prevent duplicate entries
        if not self.followers.filter(id=follower.id):
            self.followers.add(follower)

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
        follower = self._get_cached_author(follower)
        # Prevent duplicate entries
        if not self.friends.filter(id=follower.id):
            self.friends.add(follower)


    def remove_follower(self, follower):
        follower = self._get_cached_author(follower)
        self.followers.remove(follower)
        self.remove_friend(follower)

        # Remove from friends lists for users who friended self
        try:
            oldfriend = Author.objects.get(id=follower.id)
            oldfriend.remove_friend(self)
        except:
            # This will fail if:
            #   1. The friend is actually foreign hosted
            pass

    # Call remove_follower instead (if you remove a friend, your remove a follower)
    def remove_friend(self, friend):
        friend = self._get_cached_author(friend)
        self.friends.remove(friend)

    def remove_following(self, following):
        following = self._get_cached_author(following)
        self.remove_friend(following)
        self.following.remove(following)

    def __unicode__(self):
        return u'%s' % self.user.username


# Allows the integration of foreign and home authors into friend/follower
# relations. A denormalization of sorts.
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
