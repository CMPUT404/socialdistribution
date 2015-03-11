from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User

from author.models import Author, FriendRelationship
from timeline.models import Post, Comment, ACL
from timeline.views import GetPosts, CreatePost
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

import uuid
import json

# To send HTTP requests
c = APIClient()

# Values to be inserted and checked in the Author model
USERNAME = "programmer"
GITHUB_USERNAME = "programmer"
BIO = "This is my witty biography!"
HOST = "http://example.com/"

# Values to be inserted and checked in the User model
# required User model attributes

USER_A = {"username":"User_A", "password":uuid.uuid4()}
USER_B = {"username":"User_B", "password":uuid.uuid4()}
USER_C = {"username":"User_C", "password":uuid.uuid4()}
USER_D = {"username":"User_D", "password":uuid.uuid4()}
ACL_DEFAULT = {"permissions":300}
ACL_PUBLIC = {"permissions":200}
# Values to be inserted and checked in the Author model

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

        self.acl = ACL.objects.create(**ACL_DEFAULT)
        self.user_a = User.objects.create_user(**USER_A)
        self.user_a.save()
        self.user_b = User.objects.create_user(**USER_B)
        self.user_b.save()
        self.user_c = User.objects.create_user(**USER_C)
        self.user_c.save()

        self.author_a = Author.objects.create(user = self.user_a,
            github_username = GITHUB_USERNAME + "A",
            bio = BIO + "A",
            host = HOST)

        self.author_b = Author.objects.create(
            user = self.user_b,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST)
        self.author_c = Author.objects.create(
            user = self.user_c,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST)

        self.user_dict = {
            "username":USERNAME,
            "first_name":FIRST_NAME,
            "last_name":LAST_NAME,
            "password":PASSWORD,
            "email":EMAIL,
            "github_username":GITHUB_USERNAME,
            "bio":BIO }

        self.post = Post.objects.create(text = TEXT,
            author = self.author_a, acl=self.acl)

        # Set login headers for test use, or force authentication to bypass
        token, created = Token.objects.get_or_create(user=self.user_a)
        self.auth_headers = {
            "HTTP_AUTHORIZATION": "Token %s" %token }

        tokenc, createdc = Token.objects.get_or_create(user=self.user_c)
        self.auth_headers_c = {
            "HTTP_AUTHORIZATION": "Token %s" %tokenc }

    def tearDown(self):
        """Remove all created objects from mock database"""
        Author.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()
        ACL.objects.all().delete()
        Token.objects.all().delete()

    def pretty_print_dict(self, data):
        """Pretty prints a dictionary object"""
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    # DRY Utility Call
    def create_friends(self, fof = False):
        """
        Create Friends and Friends of Friends and associated posts

        If fof set to True, the created FoF will be retuned as a User Model
        """
        FriendRelationship.objects.create(friendor = self.author_b, friend = self.author_a)
        FriendRelationship.objects.create(friendor = self.author_c, friend = self.author_a)

        pac_1 = ACL.objects.create(**ACL_PUBLIC)
        pac_2 = ACL.objects.create(**ACL_PUBLIC)

        Post.objects.create(text = TEXT + "B", author = self.author_b, acl = pac_1)
        Post.objects.create(text = TEXT + "C", author = self.author_c, acl = pac_2)

        if fof:
            return self.create_friend_of_friends()

    # DRY Utility Call
    def create_friend_of_friends(self):
        user_d = User.objects.create_user(**USER_D)
        user_d.save()

        author_d = Author.objects.create(
            user = user_d,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST)
        author_d.save()

        pac_3 = ACL.objects.create(**ACL_PUBLIC)

        FriendRelationship.objects.create(friendor = author_d, friend = self.author_b)
        Post.objects.create(text = TEXT + "D", author = author_d, acl = pac_3)

        return user_d

    # DRY Utility Call
    def check_user_in_timeline(self, usernames, posts):
        """Compares a list of post's usernames against a list of usernames

        Takes as input a list of usernames and a list of posts
        """
        post_users = []
        for post in posts:
            post_users.append(post['author']['displayname'])

        for username in usernames:
            self.assertTrue(username in post_users, "%s not in timeline"\
                %username)


    def test_set_up(self):
        """Assert that that the models were created in setUp()"""
        try:
            user = User.objects.get(username = USER_A["username"])
            user = User.objects.get(id = self.user_a.id)
        except:
            self.assertFalse(True, "Error retrieving %s from database" %USER_A["username"])
        try:
            post = Post.objects.get(id = self.post.id)
        except:
            self.assertFalse(True, "Error retrieving post %s from database" %self.post.id)

    def test_get_post_by_author_from_db(self):
        """Post created in setUp() can be retrieved using Author id from setUp()"""
        post = Post.objects.get(author = self.author_a)
        self.assertEquals(post.text, TEXT)

        # If this doesn"t pass, then the following test will obviously fail

    def test_get_posts_by_author_with_http(self):
        id = self.author_a.id
        response = c.get("/author/%s/posts" %id, content_type="application/json", **self.auth_headers)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1, "Only one post should have been retrieved")

        post = response.data['posts'][0]

        self.assertEquals(post["author"]["displayname"], USER_A["username"], "Wrong post author")
        self.assertEquals(post["text"], TEXT, "Wrong post content")

    def test_get_multiple_posts_by_author_with_http(self):
        # Create two posts, in addition to the post created in setUp()
        Post.objects.create(text = TEXT, author = self.author_a, acl=ACL.objects.create(**ACL_DEFAULT))
        Post.objects.create(text = TEXT, author = self.author_a, acl=ACL.objects.create(**ACL_DEFAULT))

        id = self.author_a.id
        response = c.get("/author/%s/posts" %id, content_type="application/json", **self.auth_headers)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['posts']), 3, "Three posts should have been retrieved")

        post_ids = []

        # With the exception of post id, every post has the same text
        for post in response.data['posts']:
            post_ids.append(post["id"])
            self.assertEquals(post["text"], TEXT, "Wrong post content")

        # Ensure each post has a different id
        self.assertEquals(len(post_ids), len(set(post_ids)), "Post ids are the same for multiple posts!")

    def test_get_posts_of_friend(self):
        # Add Friends
        FriendRelationship.objects.create(friend = self.author_b, friendor = self.author_a)
        FriendRelationship.objects.create(friend = self.author_a, friendor = self.author_b)

        # Add Posts
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**ACL_DEFAULT))
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**ACL_DEFAULT))

        id = self.author_b.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 200)

        # TODO this test needs to be completed when auth is fully setup
        # Check content received by response
        # Should conform to IsOwner and IsFriend permission classes
        # See milestone 1 on issue tracker

    def test_get_posts_of_non_friend(self):
        # Add Posts
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**ACL_DEFAULT))
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**ACL_DEFAULT))

        id = self.author_b.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 403)

    def test_get_posts_of_fof(self):
        # Add Friends
        FriendRelationship.objects.create(friend = self.author_b, friendor = self.author_a)
        FriendRelationship.objects.create(friend = self.author_a, friendor = self.author_b)

        FriendRelationship.objects.create(friend = self.author_b, friendor = self.author_c)
        FriendRelationship.objects.create(friend = self.author_c, friendor = self.author_b)

        # Add Posts
        acl = {"permissions":302, "shared_users":[]}
        Post.objects.create(text = TEXT, author = self.author_c, acl=ACL.objects.create(**acl))
        Post.objects.create(text = TEXT, author = self.author_c, acl=ACL.objects.create(**acl))

        id = self.author_c.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 200)


    def test_attempt_get_posts_of_fof(self):
        # Add Friends
        FriendRelationship.objects.create(friend = self.author_b, friendor = self.author_a)
        FriendRelationship.objects.create(friend = self.author_a, friendor = self.author_b)

        FriendRelationship.objects.create(friend = self.author_b, friendor = self.author_c)
        FriendRelationship.objects.create(friend = self.author_c, friendor = self.author_b)

        # Add Posts
        acl = {"permissions":300, "shared_users":[]}
        Post.objects.create(text = TEXT, author = self.author_c, acl=ACL.objects.create(**acl))
        Post.objects.create(text = TEXT, author = self.author_c, acl=ACL.objects.create(**acl))

        id = self.author_c.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 403)

    def test_get_posts_in_private_list(self):
        # Add Posts
        acl = {"permissions":500, "shared_users":[str(self.author_a.id)]}
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**acl))

        id = self.author_b.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 200)

    def test_attempt_get_posts_in_private_list(self):
        # Add Posts
        acl = {"permissions":500, "shared_users":[str(self.author_c.id)]}
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**acl))
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**acl))

        id = self.author_b.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 403)

    def test_get_private_post(self):
        # Add Posts
        acl = {"permissions":100, "shared_users":[]}
        Post.objects.create(text = TEXT, author = self.author_a, acl=ACL.objects.create(**acl))
        Post.objects.create(text = TEXT, author = self.author_a, acl=ACL.objects.create(**acl))

        id = self.author_a.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 200)

    def test_attempt_get_private_post(self):
        # Add Posts
        acl = {"permissions":100, "shared_users":[]}
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**acl))
        Post.objects.create(text = TEXT, author = self.author_b, acl=ACL.objects.create(**acl))

        id = self.author_b.id
        response = c.get("/author/%s/posts" %id, **self.auth_headers)
        self.assertEquals(response.status_code, 403)


    def test_create_post(self):
        ptext = TEXT + " message"
        acl = {"permissions":300, "shared_users":[]}
        response = c.post("/author/post", json.dumps({"text":ptext, "acl": acl}), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)

        # Retrieve post manually to confirm
        result = Post.objects.get(text = ptext, id=response.data["id"])
        self.assertEquals(result.text, ptext, "wrong post text")

        self.assertEquals(result.author.id, self.author_a.id, "wrong user")

    def test_attempt_set_read_only_fields(self):
        """Read only fields should be ignored in POST request"""
        acl = {"permissions":300, "shared_users":["user_a"]}
        post = {"text":TEXT, "id":4, "date":"2015-01-01",
            "acl":acl}
        response = c.post("/author/post", json.dumps(post), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        # Ensure that fields were not set
        self.assertTrue(response.data["id"] != 4, "ID was set; should not have been")
        self.assertTrue(response.data["date"] != "2015-01-01")

    def test_create_blank_post(self):
        """Should not be able to create post with no text"""
        response = c.post("/author/post", {}, content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 400)

    def test_public_post_set(self):
        """public and fof are False by default"""
        post = Post.objects.create(text = TEXT,
            author = self.author_a, acl = ACL.objects.create(**ACL_DEFAULT))
        self.assertEquals(post.acl.permissions, 300)

    def test_create_public_post_http(self):
        acl = {"permissions":200, "shared_users":[]}
        post = {"text":TEXT, "acl":acl}
        response = c.post("/author/post", json.dumps(post), content_type="application/json", **self.auth_headers)

        self.assertEquals(response.status_code, 201)
        #self.assertTrue(response.data["acl"]["permissions"] == 200, "privacy not marked public")

    def test_add_comment_to_public_post(self):
        acl = {"permissions":200, "shared_users":[]}
        post = {"text":TEXT, "acl":acl}
        response = c.post('/author/post', json.dumps(post), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        # get the post id
        post_id = Post.objects.all()[0].id
        comment = {"text":TEXT}
        # comment on the post
        response = c.post('/author/posts/%s/comments' %post_id, json.dumps(comment), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        comment_id = response.data['id']
        # get the comment and ensure data is as expected
        response = c.get('/author/posts/comments/%s' %comment_id, **self.auth_headers)
        self.assertEquals(response.data['text'], TEXT)

    def test_delete_comment(self):
        acl = {"permissions":200, "shared_users":[]}
        post = {"text":TEXT, "acl":acl}
        response = c.post('/author/post', json.dumps(post), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        # get the post id
        post_id = Post.objects.all()[0].id
        comment = {"text":TEXT}
        # comment on the post
        response = c.post('/author/posts/%s/comments' %post_id, json.dumps(comment), content_type="application/json", **self.auth_headers)
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
        acl = {"permissions":200, "shared_users":[]}
        post = {"text":TEXT, "acl":acl}
        response = c.post('/author/post', json.dumps(post), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        # get the post id
        post_id = Post.objects.all()[0].id
        comment = {"text":TEXT}
        # comment on the post
        response = c.post('/author/posts/%s/comments' %post_id, json.dumps(comment), content_type="application/json", **self.auth_headers)
        self.assertEquals(response.status_code, 201)
        # get the post
        response = c.get('/author/%s/posts/%s' %(self.author_a.id, post_id), **self.auth_headers)
        self.assertEquals(response.data['posts'][0]['comments'][0]['text'], TEXT)

    def test_create_post_no_auth(self):
        response = c.post('/author/post', {'text':TEXT})
        self.assertEquals(response.status_code, 401)

    def test_retrieve_timeline_own(self):
        # Timeline will include only posts by the auth user
        response = c.get('/author/timeline', **self.auth_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)['posts']

        self.assertEquals(len(data), 1, "Too many posts returned")
        self.assertEquals(data[0]['text'], unicode(TEXT), 'Wrong post text')
        self.assertEquals(data[0]['author']['displayname'], self.user_a.username)

        # self.pretty_print_dict(data)

    def test_retrieve_multiple_posts_timeline(self):
        # Test the retrieval of multiple posts in the timeline
        acl = {"permissions":200, "shared_users":[]}
        for i in range(5):
            acl = ACL.objects.create(**ACL_PUBLIC)
            Post.objects.create(text = TEXT, author = self.author_a, acl=acl)

        response = c.get('/author/timeline', **self.auth_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)['posts']
        self.assertEquals(len(data), 6)

        # self.pretty_print_dict(data)

        # All posts are unique
        post_ids = []
        for post in data:
            post_ids.append(post['id'])
        self.assertEquals(len(data), len(set(post_ids)), "All ids are not unique")

    def test_timeline_includes_friends(self):
        self.create_friends()

        response = c.get('/author/timeline', **self.auth_headers)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)['posts']

        self.assertEquals(len(data), 3, "Wrong # of posts returned")

        users = [
            self.user_a.username,
            self.user_b.username,
            self.user_c.username ]

        self.check_user_in_timeline(users, data)

        # self.pretty_print_dict(data)

    def test_timeline_include_fof(self):
        fof = self.create_friends(True)

        response = c.get('/author/timeline', **self.auth_headers)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)['posts']

        self.assertEquals(len(data), 4, "Wrong # of posts returned")

        users = [
            self.user_a.username,
            self.user_b.username,
            self.user_c.username,
            fof.username ]

        self.check_user_in_timeline(users, data)

        self.pretty_print_dict(data)

    def test_retrieve_timeline_bogus_user(self):
        self.auth_headers = {
            'HTTP_AUTHORIZATION': "Token %s" % '19292939' }

        response = c.get('/author/timeline', **self.auth_headers)
        self.assertEquals(response.status_code, 401)

    def test_comments_in_timeline(self):
        # comment on the post
        post_id = self.post.id
        comment = {"text":TEXT + " COMMENT"}

        response = c.post('/author/posts/%s/comments' %post_id,
            json.dumps(comment), content_type="application/json",
            **self.auth_headers_c)

        self.assertEquals(response.status_code, 201)

        # Comments should be embedded in posts
        response = c.get('/author/timeline', **self.auth_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)['posts']

        self.assertEquals(len(data), 1, "Too many posts returned")
        self.assertEquals(data[0]['text'], unicode(TEXT), 'Wrong post text')
        self.assertEquals(data[0]['author']['displayname'], self.user_a.username)

        # Comment data
        self.assertEquals(data[0]['comments'][0]['author']['displayname'],
            self.user_c.username, "Wrong username in comment")

        # self.pretty_print_dict(data)
