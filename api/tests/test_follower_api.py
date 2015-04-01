from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from ..models.author import (
    Author,
    CachedAuthor)
import uuid
from ..utils import scaffold as s
from api_settings import settings

c = APIClient()

# Values to be inserted and checked in the Author model
GITHUB_USERNAME = "gituser"
BIO = "This is my witty biography!"
HOST = settings.HOST

# required User model attributes
USERNAME = "ausername"
PASSWORD = uuid.uuid4()

USER = {'username':USERNAME, 'password':PASSWORD }
USER_A = {'username':"User_A", 'password':uuid.uuid4()}
USER_B = {'username':"User_B", 'password':uuid.uuid4()}
USER_C = {'username':"User_C", 'password':uuid.uuid4()}
USER_D = {'username':"User_D", 'password':uuid.uuid4()}
USER_E = {'username':"User_E", 'password':uuid.uuid4()}

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

    # test following local author
    def test_follow_author(self):
        request = {
            "author":{
                "id":self.author.id,
                "host":HOST,
                "displayname":self.author.user.username,
            },
            "following":{
                "id":self.author_a.id,
                "host": HOST,
                "displayname":self.author_a.displayname,
            }
        }

        response = self.client.post('/author/%s/follow' % self.author.id, request)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(1, len(self.author.following.all()), "Author follws author_a")
        self.assertTrue(self.author.is_following(self.author_a), "Author does not follow author_a")

    def test_follow_remote_author(self):
        fid = str(uuid.uuid4())
        request = {
            "author":{
                "id":self.author.id,
                "host":HOST,
                "displayname":self.author.user.username,
            },
            "following":{
                "id":fid,
                "host": HOST,
                "displayname":"remoteauthor",
            }
        }
        response = self.client.post('/author/%s/follow' % self.author.id, request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(1, len(self.author.following.all()), "Author follws author_a")

        try:
            cached = CachedAuthor.objects.get(id=fid)
            self.assertTrue(self.author.is_following(cached), "Author does not follow foreign author")
        except:
            self.assertFalse(True, "Cached author for following was never created")

    def test_delete_follow(self):
        # Author is now following author_a
        self.author.follow(self.author_a)

        response = self.client.delete('/author/%s/follow/%s' %(self.author.id, self.author_a.id))
        self.assertEquals(response.status_code, 200, "Follower deleted")

        # author_a shouldn't be in an follow, pending or friend list
        self.assertFalse(self.author.has_sent_friend_request_to(self.author_a))
        self.assertFalse(self.author.is_friend(self.author_a))
        self.assertFalse(self.author.is_following(self.author_a))

    def test_delete_bad_auth(self):
        self.author.follow(self.author_a)

        response = self.client_b.delete('/author/%s/follow/%s' %(self.author.id, self.author_a.id))
        self.assertEquals(response.status_code, 401, "Follower deleted")

    def test_are_friends(self):
        user_c, author_c = s.create_author(USER_C, AUTHOR_PARAMS)
        user_d, author_d = s.create_author(USER_D, AUTHOR_PARAMS)
        user_e, author_e = s.create_author(USER_E, AUTHOR_PARAMS)
        s.create_friends(self.author, [author_c, author_d], False)

        request = {
            "query": "friends",
            "author": str(self.author.id),
            "authors": [
                str(author_c.id),
                str(author_d.id),
                str(author_e.id)
            ]
        }

        response = self.client.post('/friends/%s/' % self.author.id, request)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.data['query'] == 'friends')
        self.assertTrue(len(response.data['friends']) == 2)
        self.assertTrue(response.data['author'] == self.author.id)
        self.assertTrue(str(author_c.id) in response.data['friends'])
        self.assertTrue(str(author_d.id) in response.data['friends'])
        self.assertTrue(str(author_e.id) not in response.data['friends'])

    def test_delete_friend_through_model(self):
        self.author_a.add_friend(self.author_b)
        self.author_b.add_friend(self.author_a)

        # Confirm that A/B follow each other and thus are friends
        self.assertTrue(self.author_a.is_friend(self.author_b))
        self.assertTrue(self.author_b.is_friend(self.author_a))

        self.assertTrue(self.author_a.is_following(self.author_b))
        self.assertTrue(self.author_b.is_following(self.author_a))

        # This will remove the friendship. Follower/Friendship are dependents
        # Other author should no longer be a friend either
        self.author_a.remove_friend(self.author_b)
        self.assertEquals(0, len(self.author_a.friends.all()))
        self.assertEquals(0, len(self.author_b.friends.all()))

        # Other author should still have follow relationship
        self.assertEquals(1, len(self.author_b.following.all()))

        # Author a should have no followers or friends
        self.assertEquals(0, len(self.author_a.friends.all()))

    def test_http_unfollow_after_friendship(self):
        self.author.add_friend(self.author_b)
        self.author_b.add_friend(self.author)

        response = self.client.delete('/author/%s/follow/%s' %(self.author.id, self.author_b.id))
        self.assertEquals(response.status_code, 200, "deleted friendship/followship")

        # author should have no friends and not be following
        self.assertEquals(0, len(self.author.following.all()))
        self.assertEquals(0, len(self.author.friends.all()))

        # b should still follow a, but not be friends or be followed by a
        self.assertEquals(0, len(self.author_b.friends.all()))

    def test_api_friend_request_only_follow(self):
        request = {
            "query":"friendrequest",
            "author":{
                "id":self.author.id,
                "host":HOST,
                "displayname":self.author.user.username,
            },
            "friend":{
                "id":self.author_a.id,
                "host": HOST,
                "displayname":self.author_a.displayname,
            }
        }
        response = self.client.post('/friendrequest', request)
        self.assertEquals(response.status_code, 200)

        # This should have created only a following and request status
        self.assertEquals(0, len(self.author.friends.all()))
        self.assertEquals(1, len(self.author.following.all()))
        self.assertEquals(1, len(self.author.pending.all()))

        self.assertEquals(1, len(self.author_a.requests.all()))
        self.assertEquals(0, len(self.author_a.following.all()))
        self.assertEquals(0, len(self.author_a.pending.all()))
        self.assertEquals(0, len(self.author_a.friends.all()))

    def test_api_friend_request(self):
        self.author.add_friend(self.author_a)
        request = {
            "query":"friendrequest",
            "author":{
                "id":self.author_a.id,
                "host":HOST,
                "displayname":self.author_a.user.username
            },
            "friend":{
                "id":self.author.id,
                "host": HOST,
                "displayname":self.author.displayname,
            }
        }
        response = self.client.post('/friendrequest', request)
        self.assertEquals(response.status_code, 200)

        # This should have created the friendship as author already follows author_a
        self.assertEquals(1, len(self.author.following.all()))
        self.assertEquals(0, len(self.author.pending.all()))
        self.assertEquals(1, len(self.author.friends.all()))

        self.assertEquals(0, len(self.author_a.requests.all()))
        self.assertEquals(1, len(self.author_a.friends.all()))

    def test_friend_pending(self):
        """
        When friending an author, if they haven't sent you a request, then
        you follow them and send a request.
        """
        self.author_a._add_request_from_and_to(self.author)

        # author_a should have a pending friend and be following author
        self.assertTrue(self.author_a.has_sent_friend_request_to(self.author))
        self.assertTrue(self.author_a.is_following(self.author))
        self.assertFalse(self.author_a.is_friend(self.author))

        # Make sure no changes were made to the author, except that
        # he should now have a friend request.
        self.assertEquals(0, len(self.author.friends.all()))
        self.assertEquals(0, len(self.author.pending.all()))
        self.assertEquals(0, len(self.author.following.all()))
        self.assertEquals(1, len(self.author.requests.all()))

    def test_api_get_friends(self):
        self.author.add_friend(self.author_a)
        self.author.add_friend(self.author_b)
        self.author_a.add_friend(self.author)
        self.author_b.add_friend(self.author)

        # These friends should not show up in response
        self.author.follow(self.author_b)
        self.author_b.follow(self.author)

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
        self.author.follow(self.author_a)

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

    def test_accept_friend_request(self):
        """
        If an author accepts a friend request, the author should be removed
        from the friends pending list, and the friend should be removed
        from the author's requests list.
        """
        # Friend author and then check that author has a friend request
        self.author_a.add_friend(self.author)

        self.assertTrue(self.author.has_friend_request_from(self.author_a))
        self.assertFalse(self.author.is_following(self.author_a))
        self.assertTrue(self.author_a.is_following(self.author))
        self.assertTrue(self.author_a.has_sent_friend_request_to(self.author))

        self.author.add_friend(self.author_a)

        # Authors should appear on each others friends list
        self.assertTrue(self.author_a.is_friend(self.author))
        self.assertTrue(self.author.is_friend(self.author_a))

    def test_foreign_host_friend_request(self):
        request = {
            "query": "friendrequest",
            "author": {
                "id": str(uuid.uuid4()),
                "host": "http://example.org",
                "displayname": "foreignauthorname"
            },
            "friend": {
                "id": self.author.id,
                "host": HOST,
                "displayname": self.author.displayname,
            }
        }
        response = self.client.post('/friendrequest', request,
                                    **{'HTTP_ORIGIN': 'http://example.org'})
        self.assertEquals(response.status_code, 200)

        try:
            friend = CachedAuthor.objects.get(id=request['author']['id'])
        except:
            self.assertFalse(True, "Cached author friend should have been made")

        self.assertTrue(self.author.has_friend_request_from(friend))
