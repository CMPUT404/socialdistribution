from django.test import TestCase, Client
from django.contrib.auth.models import User
from external.models import Server
from author.models import (
    UserDetails,
    FriendRelationship,
    FriendRequest,
    FollowerRelationship )

import uuid
import json

from rest_framework.authtoken.models import Token

c = Client()

# Values to be inserted and checked in the UserDetails model
GITHUB_USERNAME = "gituser"
BIO = "This is my witty biography!"

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

class UserDetailsModelAPITests(TestCase):
    """
    Basic testing of the UserDetails model creation and database insertion
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
        self.server = Server.objects.create(address='example.com')
        self.user_details = UserDetails.objects.create(
            user = self.user,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            server = self.server)

        token, created = Token.objects.get_or_create(user=self.user_a)
        self.auth_headers_user_a = {
            'HTTP_AUTHORIZATION': "Token %s" %token }

        token, created = Token.objects.get_or_create(user=self.user_b)
        self.auth_headers_user_b = {
            'HTTP_AUTHORIZATION': "Token %s" %token }

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
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

    def test_new_follower(self):
        """
        Follow a user
        """
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)

    def test_new_follower_added(self):
        """
        Ensure the follower relationship was created
        """
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/followers/%s' %self.user_a.username)
        self.usernames_in_response(response.data['followers'], [self.user_b.username])

    def test_not_friends_yet(self):
        """
        Ensure the newly followed user is not yet a friend of the follower
        """
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/followers/%s' %self.user_a.username)
        self.usernames_in_response(response.data['followers'], [self.user_b.username])
        response = c.get('/author/friends/%s' %self.user_a.username)
        self.assertTrue(self.user_b.username not in response.data['friendors'])

    def test_follow_back(self):
        """
        Follow back the new follower and ensure a new friend relationship
        is created
        """
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/followers/%s' %self.user_a.username)
        self.usernames_in_response(response.data['followers'], [self.user_b.username])
        response = c.get('/author/friends/%s' %self.user_a.username)
        self.assertTrue(self.user_b.username not in response.data['friendors'])
        post = {'follower':self.user_a.username}
        response = c.post('/author/followers/%s' %self.user_b.username, post, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 201)

    def test_user_a_now_friend(self):
        """
        Ensure the users who have now both followed each other are friends
        """
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/followers/%s' %self.user_a.username)
        self.usernames_in_response(response.data['followers'], [self.user_b.username])
        response = c.get('/author/friends/%s' %self.user_a.username)
        self.assertTrue(self.user_b.username not in response.data['friendors'])
        post = {'follower':self.user_a.username}
        response = c.post('/author/followers/%s' %self.user_b.username, post, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/friends/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_a.username in response.data['friendors'])


    def test_users_now_friends_not_followers(self):
        """
        Ensure the users who have now both followed each other are friends
        """
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/followers/%s' %self.user_a.username)
        self.usernames_in_response(response.data['followers'], [self.user_b.username])
        response = c.get('/author/friends/%s' %self.user_a.username)
        self.assertTrue(self.user_b.username not in response.data['friendors'])
        post = {'follower':self.user_a.username}
        response = c.post('/author/followers/%s' %self.user_b.username, post, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/friends/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_a.username in response.data['friendors'])
        response = c.get('/author/friends/%s' %self.user_a.username, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_b.username in response.data['friendors'])
        # ensure neither friend is still following the other
        response = c.get('/author/followers/%s' %self.user_a.username, **self.auth_headers_user_b)
        self.assertTrue(self.user_b.username not in response.data['followers'])
        response = c.get('/author/followers/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertTrue(self.user_a.username not in response.data['followers'])


    def test_unfollow_after_friendship(self):
        post = {'follower':self.user_b.username}
        response = c.post('/author/followers/%s' %self.user_a.username, post, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/followers/%s' %self.user_a.username)
        self.usernames_in_response(response.data['followers'], [self.user_b.username])
        response = c.get('/author/friends/%s' %self.user_a.username)
        self.assertTrue(self.user_b.username not in response.data['friendors'])
        post = {'follower':self.user_a.username}
        response = c.post('/author/followers/%s' %self.user_b.username, post, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 201)
        response = c.get('/author/friends/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_a.username in response.data['friendors'])
        response = c.get('/author/friends/%s' %self.user_a.username, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_b.username in response.data['friendors'])
        # ensure neither friend is still following the other
        response = c.get('/author/followers/%s' %self.user_a.username, **self.auth_headers_user_b)
        self.assertTrue(self.user_b.username not in response.data['followers'])
        response = c.get('/author/followers/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertTrue(self.user_a.username not in response.data['followers'])
        # user_a unfollow user_b
        # ensure friendship is now gone and following relationship
        # exists as user_b show now follow user_a again
        post = {"follower":self.user_a.username}
        response = c.delete('/author/followers/%s' %self.user_b, post, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 200)
        response = c.get('/author/friends/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_a.username not in response.data['friendors'])
        response = c.get('/author/friends/%s' %self.user_a.username, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_b.username not in response.data['friendors'])
        # but user_b should now follow user_a again
        response = c.get('/author/followers/%s' %self.user_a.username, **self.auth_headers_user_b)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_b.username in response.data['followers'])
        # but user_a should not be following user_b
        response = c.get('/author/followers/%s' %self.user_b.username, **self.auth_headers_user_a)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.user_a.username not in response.data['followers'])

    def usernames_in_response(self, data, usernames=None):
        """
        Test to ensure that all usernames added to relationship are in the returned data

        Called after a retrieve relationship test has passed

        usernames: a list of usernames
        data: list of usernames to be checked against
        """

        if usernames == None:
            usernames = [self.user_a.username, self.user_b.username]

        for name in usernames:
            self.assertTrue(name in data)
