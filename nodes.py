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
user = User.objects.get_or_create(username="hindlebook")
user.set_password("hindlebook")
node = Node.objects.get_or_create(
    user=user,
    host="http://hindlebook.tamarabyte.com/api/",
    foreign_username="socshizzle",
    foreign_pass="socshizzle",
    outbound=True,
    enabled=True
)

# API Public Test Credentials
test_user = User.objects.get_or_create(username="test")
test_user.set_password("test")
test_node = Node.objects.get_or_create(
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

print "DONE!"
