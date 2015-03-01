from django.test import TestCase, Client
from django.contrib.auth.models import User
from author.models import UserDetails
from external.models import Server

import uuid
import json

c = Client()

# Values to be inserted and checked in the UserDetails model
GITHUB_USERNAME = "jmaguire"
BIO = "I'm the best sports agent around!"

# Values to be inserted and checked in the User model
# required User model attributes
USERNAME = "jmaguire"
PASSWORD = uuid.uuid4()

# optional User model attributes
FIRST_NAME = "Jerry"
LAST_NAME = "Maguire"
EMAIL = "jmaguire@smi.com"

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
        self.user_dict = {
            'username':USERNAME,
            'first_name':FIRST_NAME,
            'last_name':LAST_NAME,
            'password':PASSWORD,
            'email':EMAIL,
            'github_username':GITHUB_USERNAME,
            'bio':BIO
            }

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()

    def test_registration(self):
        """
        Test a registration where all values are given in the JSON body
        """
        response = c.post('/author/registration/', self.user_dict)

        self.assertEquals(response.status_code, 201, "User and UserDetails not created")

        print response.data

        # Confirm that model and all attributes were inserted
        user = User.objects.get(username = USERNAME)
        self.assertEquals(user.username, USERNAME, "Usernames don't match")
        self.assertEquals(user.first_name, FIRST_NAME, "Name doesn't match")
        self.assertEquals(user.last_name, LAST_NAME, "Name doesn't match")

        details = UserDetails.objects.get(user = user)
        self.assertEquals(details.bio, BIO, "Bio doesn't match")
        self.assertEquals(details.github_username, GITHUB_USERNAME, "Username doesn't match")
        self.assertEquals(len(details.uuid), 32, "UUID not 32 bits")

    def test_registration_same_user(self):
        """
        Test registering the same user properties again
        """
        response = c.post('/author/registration/', self.user_dict)

        print response

    def test_registration_without_username(self):
        """
        Should not be able to register without username
        """
        self.user_dict.pop('username', None)
        response = c.post('/author/registration/', self.user_dict)

        self.assertEquals(response.status_code, 400, "User should not be created")

    def test_registration_without_email(self):
        """
        Should not be able to register without email
        """
        self.user_dict.pop('email', None)
        response = c.post('/author/registration/', self.user_dict)

        self.assertEquals(response.status_code, 400, "User should not be created")

    def test_registration_without_name(self):
        """
        Should not be able to register without names
        """
        self.user_dict.pop('first_name', None)
        response = c.post('/author/registration/', self.user_dict)

        self.assertEquals(response.status_code, 400, "User should not be created")

    def test_registration_without_github(self):
        """
        Should not be able to register without github
        """
        self.user_dict.pop('github_username', None)
        response = c.post('/author/registration/', self.user_dict)

        self.assertEquals(response.status_code, 400, "User should not be created")
