from django.test import TestCase, Client
from django.contrib.auth.models import User

from external.models import Server
from author.models import UserDetails, FriendRelationship

from timeline.models import Post, Comment

import uuid
import json

# To send HTTP requests
c = Client()

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

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()

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
        response = c.get('/author/%s/posts' %username, content_type="application/json")

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
        response = c.get('/author/%s/posts' %username, content_type="application/json")

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
        FriendRelationship.objects.create(friendor = self.user_a, friend = self.user_b)
        FriendRelationship.objects.create(friendor = self.user_a, friend = self.user_c)

        # Add Posts
        Post.objects.create(text = TEXT, user = self.user_a)
        Post.objects.create(text = TEXT, user = self.user_a)
        username = self.user_a.username

        response = c.post('/author/registration/', self.user_dict)
        self.assertEquals(response.status_code, 201, "User and UserDetails not created")
        response = c.get('/author/%s/posts' %username)
