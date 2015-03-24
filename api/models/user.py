from django.conf import settings
from django.contrib.auth.models import User
from uuidfield import UUIDField
from django.db import models

# Base API User Class
class APIUser(models.Model):

    user = models.OneToOneField(User)
    id = UUIDField(auto=True, primary_key=True)
    host = models.URLField(blank=False, null=False, default=settings.HOST)
    enabled = models.BooleanField(default=True)

    @property
    def host(self):
        return settings.HOST

    class Meta:
        abstract = True
