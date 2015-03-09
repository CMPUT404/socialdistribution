from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User

from external.models import Server
from author.models import UserDetails, FriendRelationship
from timeline.models import Post, Comment
from timeline.views import GetPosts, CreatePost
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

import uuid
import json

# To send HTTP requests
c = APIClient()

# Values to be inserted and checked in the Author model
USERNAME = 'programmer'
GITHUB_USERNAME = "programmer"
BIO = "This is my witty biography!"

# Values to be inserted and checked in the User model
# required User model attributes

USER_A = {'username':"User_A", 'password':uuid.uuid4()}
USER_B = {'username':"User_B", 'password':uuid.uuid4()}
USER_C = {'username':"User_C", 'password':uuid.uuid4()}

# Values to be inserted and checked in the UserDetails model

# optional User model attributes
FIRST_NAME = "Jerry"
LAST_NAME = "Maguire"
EMAIL = "jmaguire@smi.com"
PASSWORD = str(uuid.uuid4())


# Post attributes
TEXT = "Some post text"

class TimelineAPITestCase(TestCase):
    """
    Testing Timeline API Prototypes
    """
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user_a = User.objects.create_user(**USER_A)
        self.user_a.save()
        self.user_b = User.objects.create_user(**USER_B)
        self.user_b.save()
        self.user_c = User.objects.create_user(**USER_C)
        self.user_c.save()
        self.server = Server.objects.create(address='example.com')

        self.user_details = UserDetails.objects.create(user = self.user_a,
            github_username = GITHUB_USERNAME + 'A',
            bio = BIO + 'A',
            server = self.server)

        self.user_dict = {
            'username':USERNAME,
            'first_name':FIRST_NAME,
            'last_name':LAST_NAME,
            'password':PASSWORD,
            'email':EMAIL,
            'github_username':GITHUB_USERNAME,
            'bio':BIO }

        self.post = Post.objects.create(text = TEXT,
            user = self.user_a)

        # Set login headers for test use, or force authentication to bypass
        token, created = Token.objects.get_or_create(user=self.user_a)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': "Token %s" %token }

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()
        Token.objects.all().delete()

    def test_set_up(self):
        """Assert that that the models were created in setUp()"""
        try:
            user = User.objects.get(username = USER_A['username'])
            user = User.objects.get(id = self.user_a.id)
        except:
            self.assertFalse(True, 'Error retrieving %s from database' %USER_A['username'])
        try:
            post = Post.objects.get(id = self.post.id)
        except:
            self.assertFalse(True, "Error retrieving post %s from database" %self.post.id)

    def test_get_post_by_author_from_db(self):
        """Post created in setUp() can be retrieved using UserDetails id from setUp()"""
        post = Post.objects.get(user = self.user_a)
        self.assertEquals(post.text, TEXT)

        # If this doesn't pass, then the following test will obviously fail

    def test_get_posts_by_author_with_http(self):
        username = self.user_a.username
        response = c.get('/author/%s/posts' %username, content_type="application/json", **self.auth_headers)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1, "Only one post should have been retrieved")

        post = response.data[0]
        self.assertEquals(post['user']['username'], USER_A['username'], "Wrong post author")
        self.assertEquals(post['text'], TEXT, "Wrong post content")

    def test_get_multiple_posts_by_author_with_http(self):
        # Create two posts, in addition to the post created in setUp()
        Post.objects.create(text = TEXT, user = self.user_a)
        Post.objects.create(text = TEXT, user = self.user_a)

        username = self.user_a.username
        response = c.get('/author/%s/posts' %username, content_type="application/json", **self.auth_headers)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 3, "Three posts should have been retrieved")

        post_ids = []

        # With the exception of post id, every post has the same text
        for post in response.data:
            post_ids.append(post['id'])
            self.assertEquals(post['text'], TEXT, "Wrong post content")

        # Ensure each post has a different id
        self.assertEquals(len(post_ids), len(set(post_ids)), "Post ids are the same for multiple posts!")

    def test_get_posts_of_friend(self):
        # Add Friends
        FriendRelationship.objects.create(friend = self.user_b, friendor = self.user_a)
        FriendRelationship.objects.create(friend = self.user_a, friendor = self.user_b)

        # Add Posts
        Post.objects.create(text = TEXT, user = self.user_b)
        Post.objects.create(text = TEXT, user = self.user_b)

        username = self.user_b.username
        response = c.get('/author/%s/posts' %username, **self.auth_headers)
        self.assertEquals(response.status_code, 200)

        # TODO this test needs to be completed when auth is fully setup
        # Check content received by response
        # Should conform to IsOwner and IsFriend permission classes
        # See milestone 1 on issue tracker

    def test_get_posts_of_non_friend(self):
        # Add Posts
        Post.objects.create(text = TEXT, user = self.user_b)
        Post.objects.create(text = TEXT, user = self.user_b)

        username = self.user_b.username
        response = c.get('/author/%s/posts' %username, **self.auth_headers)
        self.assertEquals(response.status_code, 403)

    def test_create_post(self):
        ptext = TEXT + ' message'
        response = c.post('/author/post', {'text':ptext}, **self.auth_headers)
        self.assertEquals(response.status_code, 201)

        # Retrieve post manually to confirm
        result = Post.objects.get(text = ptext)
        self.assertEquals(result.text, ptext, 'wrong post text')
        self.assertEquals(result.user, self.user_a, 'wrong user')

    def test_attempt_set_read_only_fields(self):
        """Read only fields should be ignored in POST request"""
        post = {'text':TEXT, 'id':4, 'date':'2015-01-01'}
        response = c.post('/author/post', data = post, **self.auth_headers)
        self.assertEquals(response.status_code, 201)

        # Ensure that fields were not set
        self.assertTrue(response.data['id'] != 4, 'ID was set; should not have been')
        self.assertTrue(response.data['date'] != '2015-01-01')

    def test_create_blank_post(self):
        """Should not be able to create post with no text"""
        response = c.post('/author/post', {}, **self.auth_headers)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['error'], {'text': [u"This field is required."]})

    def test_public_post_set(self):
        """public and fof are False by default"""
        post = Post.objects.create(text = TEXT,
            user = self.user_a)

        self.assertEquals(post.public, False)
        self.assertEquals(post.fof, False)

    def test_create_public_post_http(self):
        post = {'text':TEXT, 'public':True, 'fof':True}
        response = c.post('/author/post', data = post, **self.auth_headers)
        self.assertEquals(response.status_code, 201)

        self.assertTrue(response.data['public'], 'privacy not marked public')
        self.assertTrue(response.data['fof'], "fof not marked public")

    def test_add_comment_to_public_post(self):
        post = {'text':TEXT, 'public':True, 'fof':True}
        response = c.post('/author/post', data = post, **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        self.assertTrue(response.data['public'], 'privacy not marked public')
        self.assertTrue(response.data['fof'], "fof not marked public")
        # get the post id
        post_id = Post.objects.all()[0].id
        comment = {'text':TEXT}
        # comment on the post
        response = c.post('/author/posts/%s/comments' %post_id, data=comment, **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        comment_id = response.data['id']
        # get the comment and ensure data is as expected
        response = c.get('/author/posts/comments/%s' %comment_id, **self.auth_headers)
        self.assertEquals(response.data['text'], TEXT)

    def test_delete_comment(self):
        post = {'text':TEXT, 'public':True, 'fof':True}
        response = c.post('/author/post', data = post, **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        self.assertTrue(response.data['public'], 'privacy not marked public')
        self.assertTrue(response.data['fof'], "fof not marked public")
        # get the post id
        post_id = Post.objects.all()[0].id
        comment = {'text':TEXT}
        # comment on the post
        response = c.post('/author/posts/%s/comments' %post_id, data=comment, **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        comment_id = response.data['id']
        # delete the comment
        response = c.delete('/author/posts/comments/%s' %comment_id, **self.auth_headers)
        self.assertEquals(response.status_code, 204)
        # ensure comment has been removed
        response = c.get('/author/posts/comments/%s' %comment_id, **self.auth_headers)
        self.assertEquals(response.status_code, 404)
        # delete a comment that does not exist
        response = c.delete('/author/posts/comments/%s' %comment_id, **self.auth_headers)
        self.assertEquals(response.status_code, 404)

    def test_get_post_with_comments(self):
        post = {'text':TEXT, 'public':True, 'fof':True}
        response = c.post('/author/post', data = post, **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        self.assertTrue(response.data['public'], 'privacy not marked public')
        self.assertTrue(response.data['fof'], "fof not marked public")
        # get the post id
        post_id = Post.objects.all()[0].id
        comment = {'text':TEXT}
        # comment on the post
        response = c.post('/author/posts/%s/comments' %post_id, data=comment, **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        # get the post
        response = c.get('/author/%s/posts/%s' %(self.user_a.username, post_id), **self.auth_headers)
        self.assertEquals(response.data[0]['comments'][0]['text'], TEXT)

    def test_create_post_no_auth(self):
        response = c.post('/author/post', {'text':TEXT})
        self.assertEquals(response.status_code, 401)