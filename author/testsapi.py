from django.test import TestCase, Client
from django.contrib.auth.models import User

from author.models import (
    Author,
    FriendRelationship,
    FriendRequest,
    FollowerRelationship )

import uuid
import json

c = Client()

# Values to be inserted and checked in the Author model
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

class AuthorModelAPITests(TestCase):
    """
    Basic testing of the Author model creation and database insertion
    """
    def setUp(self):
        """
        Creates 3 users and 3 authors.

        The main user/author is user/author.
        Secondary user/authors are user_a/author_a and user_b/author_b

        Relationships are created in their respective tests
        """
        self.user = User.objects.create_user(**USER)

        self.user_a = User.objects.create_user(**USER_A)
        self.user_b = User.objects.create_user(**USER_B)

        self.author = Author.objects.create(
            user = self.user,
            github_username = GITHUB_USERNAME,
            bio = BIO)

        self.author_a = Author.objects.create(user = self.user_a)
        self.author_b = Author.objects.create(user = self.user_b)

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
            u = User.objects.get(username = USERNAME)
        except:
            self.assertFalse(True, 'Error retrieving %s from database' %USERNAME)

        self.assertEquals(u.first_name, FIRST_NAME)
        self.assertEquals(u.last_name, LAST_NAME)
        self.assertEquals(u.email, EMAIL)

    def test_retrieve_details(self):
        response = c.get('/author/%s' %self.author.uuid, content_type="application/json")
        self.assertEquals(response.status_code, 200)

        j = get_dict_response(response)

        self.assertEquals(j[0]['user']['email'], EMAIL)

    def test_retrieve_friends(self):
        FriendRelationship.objects.create(friendor = self.author_a, friend = self.author)
        FriendRelationship.objects.create(friendor = self.author_b, friend = self.author)

        response = c.get('/author/friends/%s' %self.author.uuid)
        self.assertEquals(response.status_code, 200)

        # TODO checking response content
        # Response json can still be formatted better
        # [{"friendor":{"user":2,"uuid":"399a137745c84722b66f4ed853befca0"}},{"friendor":{"user":3,"uuid":"5f0149272bc94d039fccd53376e748c6"}}]

    def test_retrieve_requests(self):
        FriendRequest.objects.create(requestor = self.author_a, requestee = self.author)
        FriendRequest.objects.create(requestor = self.author_b, requestee = self.author)

        response = c.get('/author/friendrequests/%s' %self.author.uuid)
        self.assertEquals(response.status_code, 200)

        # TODO, same as above

    def test_retrieve_followers(self):
        FollowerRelationship.objects.create(follower = self.author_a, followee = self.author)
        FollowerRelationship.objects.create(follower = self.author_b, followee = self.author)

        response = c.get('/author/followers/%s' %self.author.uuid)
        self.assertEquals(response.status_code, 200)

        # TODO, same as above
