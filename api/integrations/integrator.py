import requests as request
from ..models import Node
from requests.auth import HTTPBasicAuth
from ..serializers import AuthorSerializer, PostSerializer

class Integrator:

    def __init__(self, node, headers={}, requestor=None):
        self.host = node.host
        self.username = node.foreign_username
        self.password = node.foreign_pass
        self.headers = headers
        self.requestor = requestor

    @staticmethod
    def build_for_author(author):
        """
        Builds an integrator that works for the provided foreign author.
        """
        node = Node.objects.get(host=author.host)
        return Integrator(node)

    @staticmethod
    def build_from_host(host):
        node = Node.objects.get(host=host)
        return Integrator(node)

    def build_url(self, endpoint):
        # Don't touch the slashes, or lack thereof, intentional.
        return "%s%s" % (self.host, endpoint)

    def build_auth(self):
        """
        Builds the authentication credentials from instance properties.
        """
        return HTTPBasicAuth(self.username, self.password)

    def request(self, method, url, data={}, headers={}):
        """
        Handles build and sending requests based on defined settings.
        """
        return method(
            url,
            headers=headers,
            auth=self.build_auth(),
            data=data
        )

    def get_public_posts(self):
        """
        Queries foreign server for /posts
        """
        response = self.request(request.get, self.build_url("posts"))
        if response.status_code == 200:
            return self.prepare_post_data(response)
        else:
            print "Error calling %s" % (self.build_url("posts"))
            return []

    def get_author(self, origin):
        """
        Queries foreign server for /author/:id
        """
        response = self.request(request.get, origin, {})
        print response
        if response.status_code == 200:
            return self.prepare_author_data(response)
        else:
            return None

    def get_author_posts(self, origin, requestor=None):
        """
        Queries foreign server for /author/:id/posts
        """
        headers = {"UUID": str(requestor)}

        response = self.request(request.get, "%s/posts" % (origin), {}, headers)
        print vars(response), "Data"
        if response.status_code == 200:
            return self.prepare_post_data(response)
        else:
            return []

    def send_friend_request(self, author, foreign_author):
        data = {
            "query": "friendrequest",
            "author": {
                "id": foreign_author.id,
                "host": foreign_author.host,
                "displayname": foreign_author.displayname
            },
            "friend": {
                "id": author.id,
                "host": author.host,
                "displayname": author.displayname,
                "url": author.url
            }
        }

        response = self.request(request.post, self.build_url("friendrequest"), data)
        if response.status_code == 201:
            return True
        else:
            return False

    def get_author_view(self, origin):
        """
        Combines together a bunch of foreign author calls to one object to help the
        frontend. Includes, author's info, friends, and posts.
        """
        author = self.get_author(origin)
        # posts = get_author_posts(author_id)
        # friends = get_author_friends(author_id)
        # author["posts"] = posts
        # author["friends"] = friends
        return author

    def get_author_view_from_id(self, id):
        return self.get_author_view(self.build_url("author/%s" % (id)))

    def prepare_post_data(self, response):
        posts = response.json()["posts"]
        for post in posts:
            post["source"] = response.url
        return posts

    def prepare_author_data(self, response):
        author = response.json()
        author["source"] = self.host
        return author
