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

    @property
    def url(self):
        return self.host + 'author/' + str(self.id)

    # Prevents type errors, when people send in Author instead of CachedAuthor
    def _get_cached_author(self, instance):
        """Returns a CachedAuthor model given either Author or CachedAuthor"""
        if isinstance(instance, Author):
            return CachedAuthor.objects.get(id=instance.id)
        return instance

    def add_following(self, following):
        following = self._get_cached_author(following)
        if not self.following.filter(id=following.id):
            self.following.add(following)

    def add_friend(self, friend):
        """Create a friend from an author model"""
        friend = self._get_cached_author(friend)

        if not self.friends.filter(id=friend.id):
            self.friends.add(friend)

        self.add_following(friend)

    def add_request(self, friend):
        friend = self._get_cached_author(friend)
        if not self.requests.filter(id=friend.id):
            self.requests.add(friend)

    def remove_friend(self, friend):
        """
        Removes local friend. And the bidirectional relationship if
        author is local. Ignores foreign relation as per specs.
        """
        friend = self._get_cached_author(friend)

        try:
            self.friends.remove(friend)
        except:
            pass

        try:
            author = Author.objects.get(id=friend.id)
            author.friends.remove(self)
        except:
            pass

    def remove_following(self, following):
        following = self._get_cached_author(following)
        try:
            self.remove_friend(following)
            self.following.remove(following)
        except:
            pass

    def remove_request(self, friend):
        friend = self._get_cached_author(friend)
        try:
            self.requests.remove(friend)
        except:
            pass

    def is_friend(self, friend_id):
        try:
            self.friends.get(id=friend_id)
            return True
        except:
            return False

    def __unicode__(self):
        return u'%s' % self.user.username


# Allows the integration of foreign and home authors into friend/follower
# relations. A denormalization of sorts.
class CachedAuthor(models.Model):
    id = UUIDField(primary_key=True)
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
