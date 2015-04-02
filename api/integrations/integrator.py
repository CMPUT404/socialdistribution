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

    def build_auth(self, displayname=None):
        """
        Builds the authentication credentials from instance properties.
        """

        if displayname:
            username = "%s:%s" % (displayname, self.username)
        else:
            username = self.username

        return HTTPBasicAuth(username, self.password)

    def request(self, method, url, json={}, local_aid=None):
        """
        Handles build and sending requests based on defined settings.
        """

        basic_auth = self.build_auth()
        headers = {}

        # big hack because of lack of standardization without making this integrator
        # a disaster
        if "http://cs410.cs.ualberta.ca:41084/api/" in url:
            basic_auth = self.build_auth(displayname="garbage")
        elif "http://hindlebook.tamarabyte.com/api/" in url:
            # basic_auth = None
            headers["Uuid"] = local_aid

        try:
            response = method(
                url,
                headers=headers,
                auth=basic_auth,
                json=json,
                timeout=2
            )
        except request.exceptions.RequestException as e:
            print vars(e)
            print "Error calling %s\n%s" % (url, e)
            return None

        if response and response.status_code == 401:
            print "Unauthorized, consult team for %s on access credentials:(%s:%s)" % (self.host, self.username, self.password)

        return response

    def get_public_posts(self):
        """
        Queries foreign server for /posts
        """
        response = self.request(request.get, self.build_url("posts"))
        if response and response.status_code == 200:
            return self.prepare_post_data(response)
        else:
            return []

    def get_author(self, id, local_author):
        """
        Queries foreign server for /author/:id
        """
        url = self.build_url("author/%s" % id)
        response = self.request(
            request.get,
            url,
            local_aid=local_author.id
        )

        if response and response.status_code == 200:
            return self.prepare_author_data(response.json())
        else:
            return None

    def get_author_posts(self, id, local_author):
        """
        Queries foreign server for /author/:id/posts
        """
        url = self.build_url("author/%s/posts" % id)
        response = self.request(
            request.get,
            url,
            local_aid=local_author.id
        )

        if response and response.status_code == 200:
            return self.prepare_post_data(response)
        else:
            return []

    def send_friend_request(self, local_author, foreign_author):
        data = {
            "query": "friendrequest",
            "author": {
                "id": str(foreign_author.id),
                "host": foreign_author.host,
                "displayname": foreign_author.displayname,
                "url": foreign_author.url
            },
            "friend": {
                "id": str(local_author.id),
                "host": local_author.host,
                "displayname": local_author.displayname,
                "url": local_author.url
            }
        }

        response = self.request(
            request.post,
            self.build_url("friendrequest"),
            json=data,
            local_aid=local_author.id
        )

        if response and response.status_code == 200:
            return True
        else:
            return False

    def get_author_view(self, id, local_author):
        """
        Combines together a bunch of foreign author calls to one object to help the
        frontend. Includes, author's info, friends, and posts.
        """
        author = self.get_author(id, local_author)

        if author:
            posts = self.get_author_posts(id, local_author)
            author["posts"] = posts
            return author
        else:
            return None

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
        """
        Unpacks post data responses into a consistent format for our backend.
        """

        # handle post array inconsistenices in other apis
        json_data = response.json()
        if "posts" in json_data:
            posts = json_data["posts"]
        else:
            posts = json_data

        # marshal and slap on expected metadata
        for post in posts:
            post["source"] = self.host
            post["author"]["host"] = self.host

        return posts

    def prepare_authors(self, response):
        authors = []
        for author in response.json():
            author["host"] = self.host
            authors.append(self.prepare_author_data(author))
        return authors

    def prepare_author_data(self, author):
        author["source"] = self.host
        return author
