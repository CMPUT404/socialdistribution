import requests as request
from rest_framework import exceptions
from ..models import Node
from requests.auth import HTTPBasicAuth

class Integrator:
    """Handles building, executing, and formatting responses from calls to
    foreign nodes.
    """
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
        return Integrator.build_from_host(author.host)

    @staticmethod
    def build_from_host(host):
        node = Node.objects.get(host=host)
        if not node:
            exceptions.NotFound(detail="No node correspoding to provided remote author host")
        return Integrator(node)

    def build_url(self, endpoint):
        # Don't touch the slashes, or lack thereof, intentional.
        return "%s%s" % (self.host, endpoint)

    def build_auth(self):
        """
        Builds the authentication credentials from instance properties.
        """
        return HTTPBasicAuth(self.username, self.password)

    def request(self, method, url, json={}, headers={}):
        """
        Handles build and sending requests based on defined settings.
        """
        try:
            return method(
                url,
                headers=headers,
                auth=self.build_auth(),
                json=json
            )
        except:
            print "Error calling %s:%s" % (method, url)
            return None

    def get_public_posts(self):
        """
        Queries foreign server for /posts
        """
        response = self.request(request.get, self.build_url("posts"))
        if response and response.status_code == 200:
            return self.prepare_post_data(response)
        else:
            # we're returning an empty list here because we dont' want to crash
            # the call if a foreign node breaks on us
            print "Error calling %s" % (self.build_url("posts"))
            return []

    def get_author(self, origin, local_author):
        """
        Queries foreign server for /author/:id
        """
        headers = {"Uuid": str(local_author.id)}
        response = self.request(request.get, origin, headers=headers)
        if response and response.status_code == 200:
            return self.prepare_author_data(response.json())
        else:
            return None

    def get_author_posts(self, origin, requestor=None):
        """
        Queries foreign server for /author/:id/posts
        """
        headers = {"Uuid": str(requestor)}

        response = self.request(request.get, "%s/posts" % (origin), headers=headers)
        if response and response.status_code == 200:
            return self.prepare_post_data(response)
        else:
            return []

    def send_friend_request(self, author, foreign_author):
        data = {
            "query": "friendrequest",
            "author": {
                "id": str(foreign_author.id),
                "host": foreign_author.host,
                "displayname": foreign_author.displayname,
                "url": foreign_author.url
            },
            "friend": {
                "id": str(author.id),
                "host": author.host,
                "displayname": author.displayname,
                "url": author.url
            }
        }

        headers = {"Uuid": str(author.id)}
        response = self.request(request.post, self.build_url("friendrequest"), json=data, headers=headers)
        if response and response.status_code == 200:
            return True
        else:
            return False

    def get_author_view(self, origin, author):
        """
        Combines together a bunch of foreign author calls to one object to help the
        frontend. Includes, author's info, friends, and posts.
        """
        author = self.get_author(origin, author)
        posts = self.get_author_posts(origin, author)
        # friends = get_author_friends(author_id)
        author["posts"] = posts
        # author["friends"] = friends
        return author

    def get_authors(self):
        """
        Fetches all authors from the server using GET /authors
        """
        response = self.request(request.get, self.build_url('authors'))
        if response and response.status_code == 200:
            return self.prepare_authors(response)
        else:
            return []

    def prepare_post_data(self, response):
        posts = response.json()["posts"]
        for post in posts:
            post["source"] = self.host
            post["author"]["source"] = self.host
        return posts

    def prepare_authors(self, response):
        authors = []
        for author in response.json():
            authors.append(self.prepare_author_data(author))
        return authors

    def prepare_author_data(self, author):
        author["source"] = self.host
        return author
