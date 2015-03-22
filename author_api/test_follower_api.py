from django.test import TestCase, Client
from django.contrib.auth.models import User
from models import (
    Author,
    CachedAuthor,
    FriendRelationship,
    FriendRequest,
    FollowerRelationship)

import uuid

from rest_framework.authtoken.models import Token

from rest_api import scaffold as s

c = Client()

# Values to be inserted and checked in the Author model
GITHUB_USERNAME = "gituser"
BIO = "This is my witty biography!"
HOST = "http://example.com/"

# required User model attributes
USERNAME = "ausername"
PASSWORD = uuid.uuid4()

USER = {'username':USERNAME, 'password':PASSWORD }
USER_A = {'username':"User_A", 'password':uuid.uuid4()}
USER_B = {'username':"User_B", 'password':uuid.uuid4()}

AUTHOR_PARAMS = {
    'github_username':GITHUB_USERNAME,
    'bio':BIO,
    'host':HOST
}

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
        self.user, self.author, self.client = s.create_authenticated_author(USER,
            AUTHOR_PARAMS)
        self.user_a, self.author_a, self.client_a = s.create_authenticated_author(USER_A,
            AUTHOR_PARAMS)
        self.user_b, self.author_b, self.client_b = s.create_authenticated_author(USER_B,
            AUTHOR_PARAMS)

        token, created = Token.objects.get_or_create(user=self.user_a)
        self.auth_headers_user_a = {
            'HTTP_AUTHORIZATION': "Token %s" %token }

        token, created = Token.objects.get_or_create(user=self.user_b)
        self.auth_headers_user_b = {
            'HTTP_AUTHORIZATION': "Token %s" %token }

    def tearDown(self):
        """Remove all created objects from mock database"""
        CachedAuthor.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()
        FriendRelationship.objects.all().delete()
        FriendRequest.objects.all().delete()
        FollowerRelationship.objects.all().delete()

    def test_follow_author(self):
        follow = {
            'id':uuid.uuid4(),
            'host':HOST,
            'displayname':USERNAME}

        response = self.client.post('/followers/%s' %self.author.id, follow)
        self.assertEquals(response.status_code, 201, "follower not created")

        # Confirm in database
        followers = self.author.followers.all()
        s.assertFollower(self, followers[0], follow['id'])

        # Foreign node CachedAuthor should be saved in local database
        s.assertCachedAuthorExists(self, follow['id'])

        # TODO
        # If you attempt to add the same follower to the author twice
        # the endpoint doesn't return a good error message

    def test_get_followers(self):
        authors = s.create_multiple_cached_authors(2, HOST, USERNAME)
        s.create_cached_author_followers(self.author, authors)

        response = self.client.get('/followers/%s' %self.author.id)
        self.assertEquals(response.status_code, 200, "Failed to get followers")

        # s.pretty_print(response.data[0])
        s.assertNumberFollowers(self, response.data[0], 2)

        # TODO should check follower guids...Have manually checked for now.

    def test_delete_follow(self):
        authors = s.create_multiple_cached_authors(2, HOST, USERNAME)
        s.create_cached_author_followers(self.author, authors)

        to_delete = {
            'id':authors[0].id
        }

        response = self.client.delete('/followers/%s' %self.author.id,
            to_delete)
        self.assertEquals(response.status_code, 204, "Follower deleted")

        # Confirm by database query
        followers = self.author.followers.all()
        self.assertEquals(len(followers), 1, "follower wasn't removed")
        self.assertEqual(followers[0].id, authors[1].id)

        # Follower should still exist in CachedAuthors
        s.assertCachedAuthorExists(self, authors[0].id)

    def test_delete_friend_through_model(self):
        self.author_a.add_follower(self.author_b)
        self.author_b.add_follower(self.author_a)

        # Confirm that A/B follow each other and thus are friends
        self.assertEquals(1, len(self.author_a.friends.all()))
        self.assertEquals(1, len(self.author_b.friends.all()))

        # This will remove the friendship. Follower/Friendship are dependents
        # Other author should no longer be a friend either
        self.author_a.remove_follower(self.author_b)
        self.assertEquals(0, len(self.author_a.friends.all()))
        self.assertEquals(0, len(self.author_b.friends.all()))

        # Other author should still have follow relationship
        self.assertEquals(1, len(self.author_b.followers.all()))

        # Author a should have no followers or friends
        self.assertEquals(0, len(self.author_a.followers.all()))

    def test_user_a_now_friend(self):
        """
        Ensure the users who have now both followed each other are friends
        """
        # author_a follows author_b and then author_b follows author_a
        self.author_a.add_follower(self.author_b)
        self.author_b.add_follower(self.author_a)

        # Confirm that A/B follow each other
        self.assertEquals(1, len(self.author_a.followers.all()))
        self.assertEquals(1, len(self.author_b.followers.all()))

        # A/B should be friends
        if not Author.objects.get(id = self.author_a.id, friends__id = self.author_b.id):
            self.assertTrue(True, "Author b should be in author a friends list")

        if not Author.objects.get(id = self.author_b.id, friends__id = self.author_a.id):
            self.assertTrue(True, "Author a should be in author b friends list")

    # This now also covers the test_follow_back from prior commit
    def test_create_friendship_through_http(self):
        """Friendship should be created when both authors follow each other"""
        self.author_a.add_follower(self.author)
        self.assertEquals(1, len(self.author_a.followers.all()))

        follow = {
            'id':self.author_a.id,
            'host':HOST,
            'displayname':USERNAME}

        response = self.client.post('/followers/%s' %self.author.id, follow)
        self.assertEquals(response.status_code, 201, "follower not created")

        # Both should be friends
        self.assertEquals(1, len(self.author_a.friends.all()))
        self.assertEquals(1, len(self.author.friends.all()))

    def test_http_unfollow_after_friendship(self):
        # author_a follows author_b and then author_b follows author_a
        self.author.add_follower(self.author_b)
        self.author_b.add_follower(self.author)

        # Confirm that A/B follow each other
        self.assertEquals(1, len(self.author.followers.all()))
        self.assertEquals(1, len(self.author_b.followers.all()))

        unfollow = {
            "id":self.author_b.id
        }
        response = self.client.delete('/followers/%s' %self.author.id, unfollow)
        self.assertEquals(response.status_code, 204, "deleted friendship/followship")

        # author should have no friends and not be following
        self.assertEquals(0, len(self.author.followers.all()))
        self.assertEquals(0, len(self.author.friends.all()))

        # b should still follow a, but not be friends
        self.assertEquals(1, len(self.author_b.followers.all()))
        self.assertEquals(0, len(self.author_b.friends.all()))

    def test_api_friend_request_only_follow(self):
        fuuid = str(uuid.uuid4())
        request = {
            "query":"friendrequest",
            "author":{
                "id":self.author.id,
                "host":HOST,
                "displayname":self.author.user.username
            },
            "friend":{
                "id":fuuid,
                "host":"http://example.org/",
                "displayname":"foreignuser",
                "url":"http://example.org/author/" + str(fuuid),
            }
        }
        response = self.client.post('/friendrequest', request)
        self.assertEquals(response.status_code, 201)

        # This should have created only a follower relationship
        self.assertEquals(1, len(self.author.followers.all()))
        self.assertEquals(0, len(self.author.friends.all()))

    def test_api_friend_request(self):
        self.author_a.add_follower(self.author)
        request = {
            "query":"friendrequest",
            "author":{
                "id":self.author.id,
                "host":HOST,
                "displayname":self.author.user.username
            },
            "friend":{
                "id":self.author_a.id,
                "host":"http://example.org/",
                "displayname":"foreignuser",
                "url":"http://example.org/author/" + str(self.author_a.id),
            }
        }
        response = self.client.post('/friendrequest', request)
        self.assertEquals(response.status_code, 201)

        # This should have created the friendship as author already follows author_a
        self.assertEquals(1, len(self.author.followers.all()))
        self.assertEquals(1, len(self.author.friends.all()))
        self.assertEquals(1, len(self.author_a.friends.all()))
        self.assertEquals(1, len(self.author_a.followers.all()))

    def test_query_manager(self):
        """If two authors are friends, the query manager should return the author"""
        # author_a follows author_b and then author_b follows author_a
        self.author.add_follower(self.author_b)
        self.author_b.add_follower(self.author)

        # Confirm that A/B follow each other
        self.assertEquals(1, len(self.author.followers.all()))
        self.assertEquals(1, len(self.author_b.followers.all()))

        try:
            # Testing the query manager here. Returns an author if two guids are friends
            author = Author.objects.all().areFriends(self.author.id, self.author_b.id)
        except:
            # exception is thrown if author does not exist in database
            self.assertFalse(True, "friendship is not valid")

    def test_api_get_friends(self):
        self.author.add_follower(self.author_a)
        self.author_a.add_follower(self.author)

        # These friends should not show up in response
        self.author.add_follower(self.author_b)
        self.author_b.add_follower(self.author)

        response = self.client.get('/friends/%s/%s' %(self.author.id, self.author_a.id))
        self.assertEquals(response.status_code, 200)
        # s.pretty_print(response.data)

        # Author's other friends should not be included in the query
        self.assertEquals(len(response.data['authors']), 2)

        # Both authors should be in the authors list
        authors = response.data['authors']
        self.assertTrue(str(self.author.id) in authors)
        self.assertTrue(str(self.author_a.id) in authors)

    def test_api_query_no_friends(self):
        self.author.add_follower(self.author_a)

        response = self.client.get('/friends/%s/%s' %(self.author.id, self.author_a.id))
        self.assertEquals(response.status_code, 200)
        # s.pretty_print(response.data)
        self.assertEquals(response.data['friends'], "NO")

    # TODO would prefer if this returned in the api format instead of a simple 404
    def test_api_query_bad_author(self):
        response = self.client.get('/friends/5f31330b5fc04e0ba2c2aa1628cd6a8c/%s'
            %self.author_a.id)
        self.assertEquals(response.status_code, 404)

    def test_api_query_bad_friend(self):
        response = self.client.get('/friends/%s/5f31330b5fc04e0ba2c2aa1628cd6a8c'
            %self.author_a.id)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['friends'], "NO")
