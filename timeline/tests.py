from django.test import TestCase, Client
from django.contrib.auth.models import User

from author.models import Author

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

        self.ud = Author.objects.create(user = self.user,
            github_username = GITHUB_USERNAME,
            bio = BIO)

        self.post = Post.objects.create(text = TEXT,
            author = self.ud)

    def tearDown(self):
        """Remove all created objects from mock database"""
        Author.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()

    def test_set_up(self):
        """Assert that that the models were created in setUp()"""
        try:
            u = User.objects.get(username = USERNAME)
            ud = User.objects.get(id = self.user.id)
        except:
            self.assertFalse(True, 'Error retrieving %s from database' %USERNAME)
        try:
            p = Post.objects.get(id = self.post.id)
        except:
            self.assertFalse(True, "Error retrieving post %s from database" %self.post.id)

    def test_get_post_by_author_from_db(self):
        """Post created in setUp() can be retrieved using Author id from setUp()"""
        p = Post.objects.get(author = self.ud)
        self.assertEquals(p.text, TEXT)

        # If this doesn't pass, then the following test will obviously fail

    def test_get_posts_by_author_with_http(self):
        response = c.get('/author/posts/%s' %self.ud.id, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['text'], TEXT, "Wrong post was retrieved")
