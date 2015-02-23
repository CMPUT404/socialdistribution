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
GITHUB_USERNAME = "mraypold"
BIO = "This is my witty biography!"

# Values to be inserted and checked in the User model
# required User model attributes
USERNAME = "raypold"
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
        post = Post.objects.get(user = self.user)
        print Post.objects.all()[0].user
        print UserDetails.objects.get(user=self.user).uuid
        response = c.get('/author/posts/%s' %UserDetails.objects.get(user=self.user).uuid, content_type="application/json")
        print response
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['text'], TEXT, "Wrong post was retrieved")
