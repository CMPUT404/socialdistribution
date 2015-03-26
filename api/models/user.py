from django.conf import settings
from django.contrib.auth.models import User
from uuidfield import UUIDField
from django.db import models

# Base API User Class
class APIUser(models.Model):
    user = models.OneToOneField(User)
    id = UUIDField(auto=True, primary_key=True)
    host = models.URLField(null=False, default=settings.HOST)
    # TODO: change this to false for production
    enabled = models.BooleanField(default=False)
    type = models.CharField(max_length=32, default="Author")

    def __setattr__(self, attr, value):
        if attr == 'type':
            if value not in ["Author", "Node"]:
                raise ValueError('User type must be "Author" or "Node"')
        super(APIUser, self).__setattr__(attr, value)

    class Meta:
        abstract = True
