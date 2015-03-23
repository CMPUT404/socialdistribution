from django.test import TestCase
from django.contrib.auth.models import User
from author_api.models import Author, FriendRelationship
from models import Post, Comment
from rest_framework.authtoken.models import Token
from rest_api import scaffold
import uuid
import os, base64
from rest_api import scaffold as s

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
USER_E = {"username":"User_E", "password":uuid.uuid4()}

# optional User model attributes
FIRST_NAME = "Jerry"
LAST_NAME = "Maguire"
EMAIL = "jmaguire@smi.com"
PASSWORD = str(uuid.uuid4())

# Post attributes
TEXT = "Some post text"

AUTHOR_PARAMS = {
    'github_username':GITHUB_USERNAME,
    'bio':BIO,
    'host':HOST
}


class ContentAPITestCase(TestCase):
    """
    Testing Content API Prototypes
    """
    def setUp(self):
        self.user_a, self.author_a, self.client = s.create_authenticated_author(USER_A,
            AUTHOR_PARAMS)

        self.user_b, self.author_b = s.create_author(USER_B, AUTHOR_PARAMS)
        self.user_c, self.author_c = s.create_author(USER_C, AUTHOR_PARAMS)

        self.post = Post.objects.create(content = TEXT,
            author = self.author_a, visibility="PUBLIC")

        self.no_auth = s.SocialAPIClient()

    def tearDown(self):
        """Remove all created objects from mock database"""
        Author.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()
        FriendRelationship.objects.all().delete()
        Token.objects.all().delete()

        self.client.credentials()

    def test_set_up(self):
        """Assert that that the models were created in setUp()"""
        try:
            user = User.objects.get(username = USER_A["username"])
            user = User.objects.get(id = self.user_a.id)
        except:
            self.assertFalse(True, "Error retrieving %s from database" %USER_A["username"])
        try:
            post = Post.objects.get(guid=self.post.guid)
        except:
            self.assertFalse(True, "Error retrieving post %s from database" %self.post.guid)

    def getImageBase64(self, path):
        """Returns a base64 encoded image for json body"""
        with open(path, 'r') as img:
            return base64.b64encode(img.read())

    def test_get_post_by_author_from_db(self):
        """Post created in setUp() can be retrieved using Author id from setUp()"""
        post = Post.objects.get(author = self.author_a)
        self.assertEquals(post.content, TEXT)

    def test_get_post(self):
        response = self.client.get('/post/%s' % self.post.guid)
        self.assertEquals(response.status_code, 200)
        s.assertPostAuthor(self, response.data, self.author_a)
        # s.pretty_print(response.data)

    def test_get_multiple_posts_by_author_with_http(self):
        # Create two posts, in addition to the post created in setUp()
        s.create_multiple_posts(self.author_a, 2, ptext = TEXT)

        a_id = self.author_a.id
        response = self.client.get("/author/%s/posts" %a_id)

        self.assertEquals(response.status_code, 200)
        s.assertNumberPosts(self, response.data, 3)

    def test_get_posts_of_friends(self):
        # This test should only return posts by author_a and not his friends
        # This creates friends and their posts (two posts in total)
        s.create_friends(self.author_a, [self.author_b, self.author_c])

        a_id = self.author_a.id
        response = self.client.get("/author/%s/posts" % a_id)
        self.assertEquals(response.status_code, 200)

        posts = response.data
        s.assertNumberPosts(self, posts, 1)
        s.assertPostAuthor(self, posts["posts"][0], self.author_a)

        # s.pretty_print(response.data)

    # def test_get_posts_of_fof(self):
        # # Add Friends and a post each
        # s.create_friends(self.author_a, [self.author_b, self.author_c], create_post = True)

        # # Create friend of friend and a post
        # user, author = s.create_author(USER_D, AUTHOR_PARAMS)
        # s.create_friends(self.author_b, [author], create_post = True)

        # # author_a should be able to retrieve posts by author created above
        # aid = author.id
        # response = self.client.get("/author/%s/posts" % aid)
        # self.assertEquals(response.status_code, 200)

        # # s.pretty_print(response.data)

        # s.assertNumberPosts(self, response.data, 1)
        # s.assertPostAuthor(self, response.data[0], author)

    # def test_attempt_get_posts_of_fof(self):
        # # Add Friends and a post each
        # s.create_friends(self.author_a, [self.author_b, self.author_c], create_post = True)

        # # Create friend of friend and a post with private permissions
        # user, author = s.create_author(USER_D, AUTHOR_PARAMS)
        # s.create_friends(self.author_b, [author], create_post = True, aclist=ACL_PRIVATE)

        # # author_a should not be able to retrieve post by author created above
        # aid = author.id
        # response = self.client.get("/author/%s/posts" %aid)
        # self.assertEquals(response.status_code, 403)

    # def test_get_posts_in_private_list(self):
        # # Add Posts
        # _acl = {"permissions":500, "shared_users":[str(self.author_a.id)]}
        # s.create_multiple_posts(self.author_b, num = 1, acl = _acl)

        # bid = self.author_b.id
        # response = self.client.get("/author/%s/posts" %bid)

        # # s.pretty_print(response.data)

        # self.assertEquals(response.status_code, 200)
        # s.assertPostAuthor(self, response.data[0], self.author_b)
        # s.assertSharedUser(self, response.data[0], self.author_a)

    # def test_attempt_get_posts_in_private_list(self):
        # # Add Posts
        # _acl = {"permissions":500, "shared_users":[str(self.author_c.id)]}
        # s.create_multiple_posts(self.author_b, num = 2, acl = _acl)

        # bid = self.author_b.id
        # response = self.client.get("/author/%s/posts" %bid)
        # self.assertEquals(response.status_code, 403)

    # def test_get_private_post_again(self):
        # # Add Posts
        # _acl = {"permissions":100, "shared_users":[]}
        # s.create_multiple_posts(self.author_a, num = 2, acl = _acl)

        # aid = self.author_a.id
        # response = self.client.get("/author/%s/posts" %aid)
        # self.assertEquals(response.status_code, 200)

        # # s.pretty_print(response.data)
        # s.assertNumberPosts(self, response.data, 3)
        # #
        # # # TODO this is a bug. At least one post should be returned
        # # # Create user to attempt to retrieve private posts
        # # user, author, client = s.create_authenticated_author(USER_D, AUTHOR_PARAMS)
        # # response = client.get("/author/%s/posts" %aid)
        # #
        # # s.assertNumberPosts(self, response.data, 1)
        # #

    # def test_attempt_get_private_post(self):
        # # Add Posts
        # _acl = {"permissions":100, "shared_users":[]}
        # s.create_multiple_posts(self.author_b, num = 2, acl = _acl)

        # bid = self.author_b.id
        # response = self.client.get("/author/%s/posts" %bid)
        # self.assertEquals(response.status_code, 403)

    def test_create_post(self):
        ptext = TEXT + " message"
        post = {
            "title": "Tst Post",
            "content": ptext,
            "contentType": "text/x-markdown",
            "visibility": scaffold.ACL_DEFAULT
        }

        response = self.client.post("/post", post)
        self.assertEquals(response.status_code, 201)

        # Retrieve post manually to confirm
        post = Post.objects.get(guid = response.data["guid"])
        if not post:
            self.assertFalse(True, "Post does not exist")

        self.assertEquals(post.content, ptext, "wrong post text")
        self.assertEquals(post.author.id, self.author_a.id, "wrong user")

    def test_create_public_post_with_image(self):
        user, author, client = s.create_authenticated_author(USER_E, AUTHOR_PARAMS)
        base64image = self.getImageBase64(os.path.dirname(__file__) + '/../test_fixtures/images/s.jpg')
        post = {"image": "data:image/jpeg;base64," + base64image,
            "title": "Tst Post",
            "content": TEXT,
            "contentType": "text/x-markdown",
            "visibility": scaffold.ACL_DEFAULT
        }
        response = self.client.post("/post", post, format='multipart')
        self.assertEquals(response.status_code, 201)
        # Get the image.
        url = response.data.get('image')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Ensure 404 on no image
        response = self.client.get('doesnt_exist.jpg')
        self.assertEquals(response.status_code, 404)

    def test_create_post_no_auth(self):
        ptext = TEXT + " message"
        post = {
            "content": ptext,
            "visibility": scaffold.ACL_DEFAULT,
        }

        response = self.no_auth.post('/post', post)
        self.assertEquals(response.status_code, 401)

    # def test_attempt_set_read_only_fields(self):
        # """Read only fields should be ignored in POST request"""
        # acl = {"permissions":300, "shared_users":["user_a"]}
        # post = {"content":TEXT, "id":4, "date":"2015-01-01",
            # "acl":acl}

        # response = self.client.post("/author/post", post)
        # self.assertEquals(response.status_code, 201)
        # self.assertTrue(response.data["guid"] != 4, "ID was set; should not have been")

    def test_create_blank_post(self):
        """Should not be able to create post with no text"""
        response = self.client.post("/post", {})
        self.assertEquals(response.status_code, 400)

    def test_public_post_set(self):
        """public and fof are False by default"""
        post = Post.objects.create(
          content = TEXT,
          author = self.author_a,
          visibility = scaffold.ACL_DEFAULT
        )
        self.assertEquals(post.visibility, scaffold.ACL_DEFAULT)

    def test_create_public_post_http(self):
        post = {
          "title": "Public Post",
          "contentType": "text/plain",
          "content": TEXT,
          "visibility": scaffold.ACL_DEFAULT
        }
        response = self.client.post("/post", post)

        self.assertEquals(response.status_code, 201)

    def test_delete_post(self):
        post = Post.objects.create(content=TEXT, author = self.author_a, visibility=scaffold.ACL_DEFAULT)

        postid = post.guid

        response = self.client.delete('/post/%s' % postid)
        self.assertEquals(response.status_code, 204)

        # ensure post has been removed
        try:
            Post.objects.get(guid=postid)
            self.assertTrue(False, "Post should not exist still")
        except:
            pass

    def test_attempt_delete_post_non_author(self):
        post = Post.objects.create(content = TEXT, author = self.author_b, visibility = scaffold.ACL_DEFAULT)
        # deny user a's request
        response = self.client.delete('/post/%s' % post.guid)
        self.assertEquals(response.status_code, 403)

    def test_add_comment_to_public_post(self):
        post = Post.objects.create(content=TEXT, author = self.author_b, visibility = scaffold.ACL_DEFAULT)

        postid = post.guid

        # comment on the post
        comment = {
          "comment": TEXT,
          "contentType": "text/x-markdown"
        }

        response = self.client.post('/post/%s/comments' % postid, comment)
        # s.pretty_print(response.data)
        self.assertEquals(response.status_code, 201)

        commentid = response.data['guid']

        # get the comment by author_a and ensure its associated post is postid
        comment = Comment.objects.get(guid = commentid)
        self.assertEquals(comment.post.guid, postid, "comment post fk does not match")
        self.assertEquals(comment.author.user.username, self.author_a.user.username)

    def test_delete_comment_by_comment_author(self):
        post, comment = s.create_post_with_comment(
            self.author_b, self.author_a, scaffold.ACL_DEFAULT, TEXT, TEXT)

        cid = comment.guid

        response = self.client.delete('/post/%s/comments/%s' % (post.guid, cid))
        self.assertEquals(response.status_code, 204)

        # ensure comment has been removed
        try:
            comment = Comment.objects.get(guid=cid)
            self.assertTrue(False, "Comment was not deleted")
        except:
            pass

    def test_attempt_delete_comment_post_author(self):
        post, comment = s.create_post_with_comment(
            self.author_b, self.author_a, scaffold.ACL_DEFAULT, TEXT, TEXT)

        cid = comment.guid
        pid = post.guid

        # delete the comment (by post author)
        response = self.client.delete('/post/%s/comments/%s' % (pid, cid))
        self.assertEquals(response.status_code, 204)

        # ensure comment has been removed
        try:
            comment = Comment.objects.get(guid=cid)
            self.assertTrue(False, "Comment was not deleted")
        except:
            pass

        # Post should still exist
        try:
            post = Post.objects.get(id = pid)
            self.assertEquals(post.author.user.id, self.author_a.user.id)
            self.assertTrue(False, "Post was deleted and should not be")
        except:
            pass

    def test_get_post_with_comments(self):
        post, comment = s.create_post_with_comment(
            self.author_a, self.author_b, scaffold.ACL_DEFAULT, TEXT, TEXT)

        pid = post.guid

        # Create one more comment
        Comment.objects.create(post = post, comment = TEXT, author = self.author_c)

        # get the post
        response = self.client.get('/post/%s' % (pid))
        self.assertEquals(response.status_code, 200)

        # s.pretty_print(response.data)

        s.assertPostAuthor(self, response.data, self.author_a)
        s.assertNumberComments(self, response.data, 2)
        s.assertAuthorsInComments(self, [self.author_b, self.author_c],
            response.data['comments'])

    # def test_retrieve_timeline_own(self):
        # response = self.client.get('/author/posts')
        # self.assertEquals(response.status_code, 200)

        # # s.pretty_print(response.data)
        # post = response.data[0]

        # s.assertNumberPosts(self, response.data, 1)
        # s.assertPostContent(self, post, unicode(TEXT))
        # s.assertPostAuthor(self, post, self.author_a)

    # def test_retrieve_multiple_posts_timeline(self):
        # # Test the retrieval of multiple posts in the timeline
        # s.create_multiple_posts(self.author_a, num = 5)

        # response = self.client.get('/author/posts')
        # self.assertEquals(response.status_code, 200)

        # # s.pretty_print(response.data)

        # s.assertNumberPosts(self, response.data, 6)
        # s.assertNoRepeatGuids(self, response.data)

    # def test_timeline_includes_friends(self):
        # s.create_friends(self.author_a, [self.author_b, self.author_c], create_post = True)

        # response = self.client.get('/author/posts')
        # self.assertEquals(response.status_code, 200)

        # authors = [
            # self.author_a,
            # self.author_b,
            # self.author_c ]

        # s.assertNumberPosts(self, response.data, 3)
        # s.assertAuthorsInPosts(self, authors, response.data)

        # # s.pretty_print(response.data)

    # def test_timeline_include_fof(self):
        # s.create_friends(self.author_a, [self.author_b, self.author_c], create_post = True)

        # # Create a friend of friend for author b
        # user, author = s.create_author(USER_D, AUTHOR_PARAMS)
        # s.create_friends(self.author_b, [author], create_post = True)

        # response = self.client.get('/author/posts')
        # self.assertEquals(response.status_code, 200)

        # # s.pretty_print(response.data)
        # s.assertNumberPosts(self, response.data, 4 )

        # authors = [
            # self.author_a,
            # self.author_b,
            # self.author_c,
            # author ]

        # s.assertAuthorsInPosts(self, authors, response.data)

    def test_retrieve_timeline_bogus_user(self):
        response = self.no_auth.get('/author/posts')
        self.assertEquals(response.status_code, 401)


