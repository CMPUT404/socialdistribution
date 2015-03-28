#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "api_settings.settings"
from api.models import Node
from django.contrib.auth.models import User
import django

django.setup()

"""
This is just a little script to make sure that we have the right credentials getting
re-installed if we have to blow away our database in a migration.
"""

# Hindlebook Creds
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

# API Public Test Credentials
test_user = User.objects.create(username="test")
test_user.set_password("test")
test_user.save()
test_node = Node.objects.create(
    user=test_user,
    # host="http://hindlebook.tamarabyte.com/api/",
    # foreign_username="socshizzle",
    # foreign_pass="socshizzle",
    host="",
    foreign_username="",
    foreign_pass="",
    outbound=False,
    enabled=True
)
test_node.save()

print "DONE!"
