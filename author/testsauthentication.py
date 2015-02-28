from django.test import TestCase, Client
from django.contrib.auth.models import User
from author.models import UserDetails
from external.models import Server

import uuid
import json

c = Client()

# Values to be inserted and checked in the UserDetails model
GITHUB_USERNAME = "mraypold"
BIO = "This is my witty biography!"

# Values to be inserted and checked in the User model
# required User model attributes
USERNAME = "raypold"
PASSWORD = uuid.uuid4()

# optional User model attributes
FIRST_NAME = "Michael"
LAST_NAME = "Raypold"
EMAIL = "raypold@ualberta.ca"

# Main user in the tests
USER = {
    'username':USERNAME,
    'first_name':FIRST_NAME,
    'last_name':LAST_NAME,
    'email':EMAIL,
    'password':PASSWORD }

# For friend, follower, and request model testing
USER_A = {'username':"User_A", 'password':uuid.uuid4()}
USER_B = {'username':"User_B", 'password':uuid.uuid4()}

# Utility function to get around funky DRF responses that use nesting
def get_dict_response(response):
    """Returns a dictionary of the http response containing a list of ordered dictionaries"""
    return json.loads(json.dumps(response.data))

class UserDetailsAuthentication(TestCase):
    """
    Basic testing of the UserDetails model creation and database insertion
    """
    def setUp(self):
        return

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()

    def test_registration(self):
        body = {
            'username':USERNAME,
            'password1':PASSWORD,
            'email':EMAIL,
            }
        response = c.post('/author/registration/', body=body, content_type="application/json")

        print response.status_code

        print User.objects.all()
