from django.db import models
from author_api.models import Author
from uuidfield import UUIDField
import ast

# TODO: use an enum here
# 100 = 'private'
# 200 = 'public'
# 300 = 'all friends'
# 301 = 'friends on same host'
# 302 = 'friends of friends'
# 500 = 'specific users'

DEFAULT_ACL = {
    "permissions": 300,
    "shared_users": []
}

ALLOWED_ACL_FLAGS = [100, 200, 300, 301, 302, 500]

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class ACL(models.Model):
    """
    ACL
    """
    permissions = models.IntegerField()
    shared_users = ListField()

    def __setattr__(self, attrname, val):
        if attrname == 'permissions':
            try:
                val = int(val)
            except:
                raise TypeError ("Permissions must be of type int or string representation of an int")
            if val not in ALLOWED_ACL_FLAGS:
                raise ValueError ("Invalid permission flag")

        super(ACL, self).__setattr__(attrname, val)

class Post(models.Model):
    """
    Post
    """
    guid = UUIDField(auto = True, primary_key = True)
    title = models.CharField(blank = True, max_length = 200)
    content = models.TextField(blank=False)
    pubDate = models.DateTimeField(auto_now_add=True, editable = False)
    acl = models.OneToOneField(ACL)
    image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(Author, blank=False, editable = False)

    def __unicode__(self):
        return u'%s %s' %(self.author.user.username, self.content)

    # Use in serializers to add url source and origin information
    # Eg, where the query came from, and where you should query next time
    @property
    def source(self):
        return None

    @property
    def origin(self):
        return None

class Comment(models.Model):
    """
    Comment

    A comment's privacy is inherited from the Post public attribute
    """
    guid = UUIDField(auto = True, primary_key = True)
    content = models.TextField(blank=False)
    pubDate = models.DateTimeField(auto_now_add=True, editable = False)
    post = models.ForeignKey('Post', related_name='comments')
    author = models.ForeignKey(Author, blank=False, editable = False)

    def __unicode__(self):
        return u'%s %s' %(self.author.username, self.content)
