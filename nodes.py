#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "api_settings.settings"
from api.models import Node
from django.contrib.auth.models import User
import django

django.setup()

user = User.objects.create(username="hindlebook")
user.set_password("hindlebook")
user.save()
node = Node.objects.create(
    user=user,
    # host="http://hindlebook.tamarabyte.com/api/",
    # foreign_username="socshizzle",
    # foreign_pass="socshizzle",
    host="http://localhost:8001/api/",
    foreign_username="test",
    foreign_pass="test",
    outbound=True,
    enabled=True
)

node.save()

print "DONE!"
