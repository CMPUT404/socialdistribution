from abc import ABCMeta
from requests.api import request
from requests.auth import HTTPBasicAuth
from ..serializers import AuthorSerializer, PostSerializer

class Integrator:
    __metaclass__ = ABCMeta

    def __init__(self, node, headers={}):
        self.host = node.host
        self.api_postfix = node.api_postfix
        self.username = node.foreign_username
        self.password = node.foreign_pass
        self.headers = headers

    def build_url(self, endpoint):
        if self.api_postfix is not None:
            base = "%s/%s" % (self.host, self.api_postfix)
        else:
            base = self.host

        return "%s/%s" % (base, endpoint)

    def build_auth(self):
        """
        Builds the authentication credentials from instance properties.
        """
        return HTTPBasicAuth(self.username, self.password)

    def request(self, method, endpoint, data={}):
        """
        Handles build and sending requests based on defined settings.
        """
        return method(
            self.build_url(endpoint),
            headers=self.headers,
            auth=self.build_auth(),
            data=data
        )

    def get_public_posts(self):
        """
        Queries foreign server for /posts
        """
        response = self.request(request.get, "posts")

        if response.status_code == 200:
            return response.json()
        else:
            print "Error calling %s/posts" % (self.host)
            return []

    def get_author(self, author_id):
        """
        Queries foreign server for /author/:id
        """
        endpoint = "author/%s" % author_id
        response = self.request(request.get, endpoint).json()
        author_serializer = AuthorSerializer(response)
        return author_serializer.data

    def get_author_posts(self, author_id):
        """
        Queries foreign server for /author/:id/posts
        """
        endpoint = "author/%s/posts" % author_id
        response = self.request(request.get, endpoint).json()["posts"]
        posts_serializer = PostSerializer(response)
        return posts_serializer.data

    def send_friend_request(self, author, foreign_author):
        data = {
            "query": "friendrequest",
            "author": {
                "id": foreign_author.id
            },
            "friend": {
                "id": author.id,
                "host": author.host,
                "displayname": author.username,
                "url": author.url
            }
        }
        response = self.request(request.post, "friendrequest", data)
        print vars(response)
        return response

    def get_author_view(self, author_id):
        """
        Combines together a bunch of foreign author calls to one object to help the
        frontend. Includes, author's info, friends, and posts.
        """
        author = get_author(author_id)
        posts = get_author_posts(author_id)
        author["posts"] = posts
        author["friends"] = friends
        return author
