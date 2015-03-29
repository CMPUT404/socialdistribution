from django.db import models
from uuidfield import UUIDField
from user import APIUser
from api_settings import settings
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

    # Who the author is following
    following = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                       related_name='following')
    # All interaction with friends should be conducted through followers
    friends = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                     related_name='friends')
    # Friend requests made to self
    requests = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                      related_name='requests')

    # Friend requests made to others
    pending = models.ManyToManyField('CachedAuthor', blank=True, null=True,
                                      related_name='pending')
    @property
    def url(self):
        return self.host + 'author/' + str(self.id)

    @property
    def displayname(self):
        return self.user.username

    # Prevents type errors, when people send in Author instead of CachedAuthor
    def _get_cached_author(self, instance):
        """Returns a CachedAuthor model given either Author or CachedAuthor"""
        if isinstance(instance, Author):
            return CachedAuthor.objects.get(id=instance.id)
        if isinstance(instance, CachedAuthor):
            return instance
        else:
            # TODO: Should be an exception
            return None

    def follow(self, author):
        author = self._get_cached_author(author)
        if not self.following.filter(id=author.id).exists():
            self.following.add(author)
            self.save()

    def add_pending(self, friend):
        """Adds a pending friend request"""
        friend = self._get_cached_author(friend)
        if not self.pending.filter(id=friend.id).exists():
            self.pending.add(friend)
            self.save()

        self.follow(friend)

    def add_friend(self, friend):
        """Create a friend from an author model"""
        friend = self._get_cached_author(friend)
        if not self.friends.filter(id=friend.id).exists():
            self.friends.add(friend)
            self.save()

        # update other status accordingly
        self.remove_pending(friend)
        self.follow(friend)

    def add_request(self, friend):
        """Registers a new friend request that our author can respond to"""
        friend = self._get_cached_author(friend)

        # if the incoming request is actually a pending friend, convert to friend
        # status
        if self.is_pending_friend(friend):
            self.add_friend(friend)

        elif not self.requests.filter(id=friend.id).exists():
            self.requests.add(friend)
            self.save()

    def remove_friend(self, friend):
        """
        Removes local friend. And the bidirectional relationship if
        author is local. Ignores foreign relation as per specs.
        """
        friend = self._get_cached_author(friend)

        try:
            self.friends.remove(friend)
            self.save()
        except:
            # TODO: some sort of logging/exception handling
            pass

        try:
            author = Author.objects.get(id=friend.id)
            author.friends.remove(self)
            self.save()
        except:
            # TODO: some sort of logging/exception handling
            pass

    def remove_following(self, following):
        following = self._get_cached_author(following)
        try:
            self.remove_friend(following)
            self.following.remove(following)
            self.remove_pending(following)
            self.save()
        except:
            # TODO: some sort of logging/exception handling
            pass

    def remove_request(self, friend):
        friend = self._get_cached_author(friend)
        try:
            self.requests.remove(friend)
            self.save()
        except:
            # TODO: some sort of logging/exception handling
            pass

    def remove_pending(self, friend):
        friend = self._get_cached_author(friend)
        try:
            self.pending.remove(friend)
            self.save()
        except:
            # TODO: some sort of logging/exception handling
            pass

    def is_local(self):
        return self.host == settings.HOST

    def is_pending_friend(self, author):
        return self.pending.filter(id=author.id).exists()

    def is_following(self, author):
        return self.following.filter(id=author.id).exists()

    def is_friend(self, author):
        return self.friends.filter(id=author.id).exists()

    def __unicode__(self):
        return u'%s' % self.user.username


# Allows the integration of foreign and home authors into friend/follower
# relations. A denormalization of sorts.
class CachedAuthor(models.Model):
    id = models.CharField(primary_key=True, max_length=60)
    host = models.URLField(blank=False, null=False, default=settings.HOST)
    displayname = models.CharField(max_length=40, blank=False, null=False)

    @property
    def url(self):
        return self.host + 'author/' + str(self.id)

    def is_local(self):
        return self.host == settings.HOST

    def get_author(self):
        # TODO: throw an exception here instead since this is being used poorly
        if self.is_local() is False:
            return None
        else:
            return Author.objects.get(id=self.id)

    # This is used for the related string field serializer
    def __unicode__(self):
        return u'%s' % self.id
