from django.db import models
from django.contrib.auth.models import User
import json
import ast
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
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True, editable = False)
    acl = models.OneToOneField(ACL)
    #acl = models.CharField(max_length=512, blank = False, default = DEFAULT_ACL)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, blank=False, editable = False)


class Comment(models.Model):
    """
    Comment

    A comment's privacy is inherited from the Post public attribute
    """
    text = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post')
