"""
Some scaffolding to help with testing

context = the unit text class (self)
"""
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APIClient,
    ForceAuthClientHandler
)
from django.contrib.auth.models import User
from ..models.author import (
    Author,
    CachedAuthor,
    FriendRelationship,
    FriendRequest,
    FollowerRelationship
)
from ..models.content import Post, Comment
import uuid
import json
import base64
import os

ACL_DEFAULT = "PUBLIC"

# Post attributes
TEXT = "Some post text"

TEST_FOLDER_RELATIVE = "/../tests"

class SocialAPIClient(APIClient):
    """
    Create APIClient with token credentials for given author.

    token (boolean) representing to creat token auth credentials.
    """

    def __init__(self, enforce_csrf_checks=False, **defaults):
        super(APIClient, self).__init__(**defaults)
        self.handler = ForceAuthClientHandler(enforce_csrf_checks)
        self._credentials = {}

    def token_credentials(self, author):
        token, created = Token.objects.get_or_create(user = author.user)
        return self.credentials(HTTP_AUTHORIZATION=("Token %s" % token))

    def basic_credentials(self, username, password):
        basic = base64.b64encode('%s:%s' %(username, password))
        return self.credentials(HTTP_AUTHORIZATION=("Basic %s" % basic))

    def bad_credentials(self, token = True):
        """Authorization header credentials are not valid"""

        # Should not match up with anything in the database
        bad_creds = str(uuid.uuid4())

        if token:
            return self.credentials(HTTP_AUTHORIZATION=("Token %s" % bad_creds))
        else:
            return self.credentials(HTTP_AUTHORIZATION=("Basic %s" % bad_creds))

def get_image_base64(path):
    """
    Returns a base64 encoded image
    """
    with open(path, 'r') as img:
        return base64.b64encode(img.read())

def get_test_image():
    return get_image_base64(
        os.path.dirname(__file__) + TEST_FOLDER_RELATIVE + '/fixtures/images/s.jpg'
    )

def clean_up_imgs(prefix, url):
    """
    Cleans up images from tests.
    """
    img_path = os.path.dirname(__file__) + '/../../' + 'images/' + prefix + '/' + url.split('/')[-1]
    os.remove(img_path)

def pretty_print(data):
    """Pretty prints a dictionary object"""
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def create_author(user_dict, author_dict):
    """Create and return an author for testing

    Takes:
        A defined author dictionary holding all author parameters,
        Access control list (or defaults to ACL_DEFAULT)

    Returns: User and Author tuple
    """
    user = User.objects.create_user(**user_dict)
    user.save()

    author_dict['user'] = user
    author = Author.objects.create(**author_dict)
    author.save()

    return (user, author)

def create_authenticated_author(user_dict, author_dict):
    user, author = create_author(user_dict, author_dict)
    client = SocialAPIClient()
    client.token_credentials(author)

    return (user, author, client)

def create_multiple_posts(author, num, ptext = TEXT, visibility = ACL_DEFAULT):
    """
    Returns a list of created posts for the given author

    num: number of posts to create
    ptext: The text that each post will contain
    """
    posts = []

    for i in range(num):
        posts.append(Post.objects.create(content = ptext, author = author, visibility=visibility))

    return posts

def authors_in_relation(context, data, authors):
    """
    Test to ensure that all authors added to relationship are in the returned data

    Called after a retrieve relationship test has passed

    authors: a list of authors expected to be in the relation
    data: a list of guids returned from the get relationship
    """
    guids = [a.id for a in authors]
    guids = map( lambda x: str(x).replace('-', ''), guids)

    for guid in guids:
        context.assertTrue(unicode(guid) in data)

def create_requestors(_requestee, requestors):
    for r in requestors:
        FriendRequest.objects.create(requestor = r, requestee = _requestee)

def create_followers(_followee, followers):
    for f in followers:
        FollowerRelationship.objects.create(follower = f, followee = _followee)

def create_friends(friend, friendors, create_post = True, visibility = ACL_DEFAULT):
    """
    Create Friends and Friends of Friends and associated posts

    Friendors: A list of author objects that will friend.
    Friend: An author object to be friended.
    Create_posts: If you want to create a post for each friend
    visibility: acl type for each post created
    """
    for friendor in friendors:
        FriendRelationship.objects.create(friendor = friendor, friend = friend)

        if create_post:
            Post.objects.create(content = TEXT, author = friendor, visibility = visibility)

def create_post_with_comment(pauthor, cauthor, visibility, ptext, ctext):
    """Takes post author, comment author and creates a post and associated comment"""

    post = Post.objects.create(content = ptext, author = pauthor, visibility=visibility)
    comment = Comment.objects.create(comment = ctext, post = post, author = cauthor)
    return (post, comment)

def assertNoRepeatGuids(context, posts):
    """Takes response.data and confirms no repeated guids (No repeated posts)"""
    guids = [p['guid'] for p in posts]
    context.assertTrue(len(set(guids)) == len(posts), "Some guids repeated")

def cross_check(context, authors, poscom):
    """
    Compares a list of authors against a list of displaynames

    Takes:
        poscom: list of posts or comments
    """
    displaynames = [x['author']['displayname'] for x in poscom]

    for author in authors:
        if author.user.username not in displaynames:
            context.assertFalse(True, "%s not in list" %author.user.username)

def assertAuthorsInPosts(context, authors, posts):
    """Cross checks a list of authors against post"""
    cross_check(context, authors, posts)

def assertAuthorsInComments(context, authors, comments):
    """Cross checks a list of authors against comments"""
    cross_check(context, authors, comments)

def assertNumberPosts(context, posts, expected):
    context.assertEquals(len(posts["posts"]), expected,
        "expected %s, got %s posts" %(expected, len(posts)))

def assertNumberComments(context, post, expected):
    context.assertEquals(len(post['comments']), expected,
        "expected %s, got %s comments" %(expected, len(post['comments'])))

def assertPostAuthor(context, post, author):
    context.assertEquals(post["author"]["displayname"], author.user.username,
        'Post author incorrect')

def assertCommentAuthor(context, comment, author):
    context.assertEquals(comment["author"]["displayname"], author.user.username,
        'Comment author incorrect')

def assertPostContent(context, post, content):
    context.assertEquals(post["content"], content, "Post text does not match")

def assertACLPermission(context, post, permission):
    context.assertEquals(post['visibility'], str(permission),
        "expected %s, got %s" %(permission, post['visibility']))

def assertSharedUser(context, post, author):
    context.assertTrue(unicode(author.id) in post["acl"]["shared_users"],
        "author not in shared users list")

def assertPostTitle(context, post, title):
    context.assertEquals(post['title'], title, "Title did not match")

def assertUserNotExist(context, name):
    try:
        user = User.objects.get(username = name)
        context.assertFalse(True, "User should not exist")
    except:
        pass

def assertUserExists(context, name):
    try:
        user = User.objects.get(username = name)
    except:
        context.assertFalse(True, "User should exist")

def assertCachedAuthorExists(context, guid):
    try:
        author = CachedAuthor.objects.get(id = guid)
    except:
        context.assertFalse(True, "CachedAuthor should exist")

def assertFollower(context, follower, guid):
    context.assertEquals(follower.id, guid)

def assertNumberFollowers(context, followers, expected):
    context.assertEquals(len(followers['followers']), expected,
        "expected %s, got %s comments" %(expected, len(followers['followers'])))

def create_cached_author_followers(author, followers):
    """Takes a list of cachedauthors and adds them to the author follower list"""
    for f in followers:
        author.followers.add(f)

def create_multiple_cached_authors(amount, host, username):
    authors = []
    for i in range(amount):
        cached = CachedAuthor(id = uuid.uuid4(), host = host, displayname = username)
        cached.save()
        authors.append(cached)
    return authors
