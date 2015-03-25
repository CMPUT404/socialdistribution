#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "api_settings.settings"
from api.models import Node
from django.contrib.auth.models import User
import django

django.setup()

user = User.objects.create()
Node.objects.get_or_create(
    user=user,
    host="http://hindlebook.tamarabyte.com",
    api_postfix="api",
    foreign_username="test",
    foreign_pass="test",
    integrated=True
)

print "DONE!"
