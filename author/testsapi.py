from django.test import TestCase, Client
from django.contrib.auth.models import User
from author.models import (
    Author,
    FriendRelationship,
    FriendRequest,
    FollowerRelationship )

import uuid
import json
from rest_framework.authtoken.models import Token

c = Client()

# Values to be inserted and checked in the Author model
GITHUB_USERNAME = "gituser"
BIO = "This is my witty biography!"
HOST = "http://example.com/"

# Values to be inserted and checked in the User model
# required User model attributes
USERNAME = "nameuser"
PASSWORD = uuid.uuid4()

# optional User model attributes
FIRST_NAME = "firstname"
LAST_NAME = "lastname"
EMAIL = "person@example.org"

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

class AuthorModelAPITests(TestCase):
    """
    Basic testing of the Author model creation and database insertion
    """
    def setUp(self):
        """
        Creates 3 users and 3 authors.

        The main user/author is user/author.
        Secondary user/authors are user_a/user_details_a and user_b/user_details_b

        Relationships are created in their respective tests
        """
        self.user = User.objects.create_user(**USER)
        self.user_a = User.objects.create_user(**USER_A)
        self.user_b = User.objects.create_user(**USER_B)
        self.author = Author.objects.create(
            user = self.user,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST)
        self.author_a = Author.objects.create(
            user = self.user_a,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST)
        self.author_b = Author.objects.create(
            user = self.user_b,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST)

        token, created = Token.objects.get_or_create(user=self.user_a)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': "Token %s" %token }

    def tearDown(self):
        """Remove all created objects from mock database"""
        Author.objects.all().delete()
        User.objects.all().delete()
        FriendRelationship.objects.all().delete()
        FriendRequest.objects.all().delete()
        FollowerRelationship.objects.all().delete()

    def test_set_up(self):
        """ Assert that that the user model was created in setUp()"""
        try:
            user = User.objects.get(username = USERNAME)
        except:
            self.assertFalse(True, 'Error retrieving %s from database' %USERNAME)

        self.assertEquals(user.first_name, FIRST_NAME)
        self.assertEquals(user.last_name, LAST_NAME)
        self.assertEquals(user.email, EMAIL)

    def test_retrieve_details(self):
        response = c.get('/author/%s' %self.author.id,
            content_type="application/json", **self.auth_headers)

        self.assertEquals(response.status_code, 200)

        user_dict = get_dict_response(response)
        self.assertEquals(user_dict['email'], EMAIL)

    def test_invalid_retrieve_details(self):
        response = c.get('/author/no_user_here', **self.auth_headers)
        self.assertEquals(response.status_code, 404)

    def test_relation_user_dne(self):
        response = c.get('/author/friends/%s' %'bogus_user')
        self.assertEquals(response.status_code, 404)

    def test_retrieve_friends(self):
        FriendRelationship.objects.create(friendor = self.author_a, friend = self.author)
        FriendRelationship.objects.create(friendor = self.author_b, friend = self.author)

        response = c.get('/author/friends/%s' %self.author.id)

        self.assertEquals(response.status_code, 200)
        self.users_in_response(response.data['friendors'])

    def test_retrieve_requests(self):
        FriendRequest.objects.create(requestor = self.author_a, requestee = self.author)
        FriendRequest.objects.create(requestor = self.author_b, requestee = self.author)

        response = c.get('/author/friendrequests/%s' %self.author.id)

        self.assertEquals(response.status_code, 200)
        self.users_in_response(response.data['requestors'])

    def test_retrieve_followers(self):
        FollowerRelationship.objects.create(follower = self.author_a, followee = self.author)
        FollowerRelationship.objects.create(follower = self.author_b, followee = self.author)

        response = c.get('/author/followers/%s' %self.author.id, **self.auth_headers)

        self.assertEquals(response.status_code, 200)
        self.users_in_response(response.data['followers'])

    def users_in_response(self, data, users=None):
        """
        Test to ensure that all usernames added to relationship are in the returned data

        Called after a retrieve relationship test has passed

        usernames: a list of usernames
        data: list of usernames to be checked against
        """

        if users == None:
            users = [self.author_a.id, self.author_b.id]

        users = map( lambda x: str(x).replace('-', ''), users)

        for name in users:
            self.assertTrue(unicode(name) in data)
