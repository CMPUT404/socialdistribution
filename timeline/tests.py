from django.test import TestCase, Client
from django.contrib.auth.models import User

from external.models import Server
from author.models import UserDetails

from timeline.models import Post, Comment

import uuid
import json

# To send HTTP requests
c = Client()

# Values to be inserted and checked in the Author model
GITHUB_USERNAME = "programmer"
BIO = "This is my witty biography!"

# Values to be inserted and checked in the User model
# required User model attributes
USERNAME = "username"
PASSWORD = uuid.uuid4()

# Post attributes
TEXT = "Some post text"

class TimelineAPITestCase(TestCase):
    """
    Testing Timeline API Prototypes
    """
    def setUp(self):
        self.user = User.objects.create_user(username = USERNAME,
            password = PASSWORD)
        self.user.save()
        self.server = Server.objects.create(address='example.com')
        self.user_details = UserDetails.objects.create(user = self.user,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            server = self.server)

        self.post = Post.objects.create(text = TEXT,
            user = self.user)

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()

    def test_set_up(self):
        """Assert that that the models were created in setUp()"""
        try:
            user = User.objects.get(username = USERNAME)
            user = User.objects.get(id = self.user.id)
        except:
            self.assertFalse(True, 'Error retrieving %s from database' %USERNAME)
        try:
            post = Post.objects.get(id = self.post.id)
        except:
            self.assertFalse(True, "Error retrieving post %s from database" %self.post.id)

    def test_get_post_by_author_from_db(self):
        """Post created in setUp() can be retrieved using UserDetails id from setUp()"""
        post = Post.objects.get(user = self.user)
        self.assertEquals(post.text, TEXT)

        # If this doesn't pass, then the following test will obviously fail

    def test_get_posts_by_author_with_http(self):
        uuid = UserDetails.objects.get(user=self.user).uuid
        response = c.get('/author/%s/posts' %uuid, content_type="application/json")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1, "Only one post should have been retrieved")

        post = response.data[0]
        self.assertEquals(post['user']['username'], USERNAME, "Wrong post author")
        self.assertEquals(post['text'], TEXT, "Wrong post content")

    def test_get_multiple_posts_by_author_with_http(self):
        # Create two posts, in addition to the post created in setUp()
        Post.objects.create(text = TEXT, user = self.user)
        Post.objects.create(text = TEXT, user = self.user)

        uuid = UserDetails.objects.get(user=self.user).uuid
        response = c.get('/author/%s/posts' %uuid, content_type="application/json")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 3, "Three posts should have been retrieved")

        post_ids = []

        # With the exception of post id, every post has the same text
        for post in response.data:
            post_ids.append(post['id'])
            self.assertEquals(post['text'], TEXT, "Wrong post content")

        # Ensure each post has a different id
        self.assertEquals(len(post_ids), len(set(post_ids)), "Post ids are the same for multiple posts!")
