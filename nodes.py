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
# https://github.com/Tamarabyte/cmput410-project
user = User.objects.create(username="hindlebook")
user.set_password("hindlebook")
user.save()
node = Node.objects.get_or_create(
    user=user,
    host="http://hindlebook.tamarabyte.com/api/",
    foreign_username="team5",
    foreign_pass="team5",
    outbound=True,
    enabled=True
)

# Nbor
# https://github.com/CMPUT410W15/cmput410-project
user = User.objects.create(username="nbor")
user.set_password("nbor")
user.save()
node = Node.objects.get_or_create(
    user=user,
    host="http://cs410.cs.ualberta.ca:41084/api/",
    foreign_username="host",
    foreign_pass="password",
    outbound=True,
    enabled=True
)

# API Public Test Credentials
test_user = User.objects.create(username="test")
test_user.set_password("test")
test_user.save()
test_node = Node.objects.get_or_create(
    user=test_user,
    host="",
    foreign_username="",
    foreign_pass="",
    outbound=False,
    enabled=True
)

print "DONE!"
