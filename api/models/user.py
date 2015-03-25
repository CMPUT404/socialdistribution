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

    class Meta:
        abstract = True
