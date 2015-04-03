from rest_framework.test import APITestCase
from api_settings import settings
from ..integrations import Aggregator
from ..models import Node, CachedAuthor
from django.contrib.auth.models import User
import uuid

class IntegrationTests(APITestCase):

    def setUp(self):
        # need to specify nodes here otherwise there won't be anything in the nodes
        # db
        # user = User.objects.create(username="nbor")
        # user.save()
        # Node.objects.get_or_create(
            # user=user,
            # host="http://cs410.cs.ualberta.ca:41084/api/",
            # foreign_username="host",
            # foreign_pass="password",
            # outbound=True
        # )

        # user = User.objects.create(username="hindlebook")
        # user.save()
        # Node.objects.get_or_create(
            # user=user,
            # host="http://hindlebook.tamarabyte.com/api/",
            # foreign_username="team5",
            # foreign_pass="team5",
            # outbound=True
        # )

        self.integrators = Aggregator.get_integrators()

    def build_author(self):
        id = uuid.uuid4()
        return CachedAuthor(
            id=id,
            host=settings.HOST,
            displayname="JimmyBob",
            url= "%sauthor/%s" % (settings.HOST, str(id))
        )

    # finds a queryable author from the public posts on a given node
    def get_available_author(self, integrator):
        test_post_set = integrator.get_public_posts()
        if test_post_set:
            # parse out an author and convert to cached author format
            data = test_post_set[0]["author"]
            print data
            return CachedAuthor(
                host=data["host"],
                id=str(data["id"]),
                displayname=data["displayname"]
            )
        else:
            self.assertFalse(True, "No posts to fetch an author from")

    def test_public_posts(self):
        count = 0
        for integrator in self.integrators:
            posts = integrator.get_public_posts()
            count += len(posts)
            self.assertTrue(isinstance(posts, list), "Expecting posts to be a list")
            self.assertEqual(len(posts) > 0, True, "No posts returned")
            self.assertEqual(integrator.host, posts[0]["source"])
            self.assertEqual(integrator.host, posts[0]["author"]["host"])

        posts = Aggregator.get_public_posts()
        self.assertTrue(isinstance(posts, list), "Expecting posts to be a list")
        self.assertTrue(posts is not None, "posts shouldn't be empty")

    def test_get_author_posts(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_posts = integrator.get_author_posts(author.id, author)
                self.assertTrue(len(author_posts) > 0, "Empty author posts")
            else:
                self.assertTrue(False, "Unable to find available author")

    def test_get_posts_for_authors(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_posts = Aggregator.get_posts_for_authors([author], self.build_author())
                self.assertTrue(type(author_posts) is list, "Expected get_author_posts to return a list")

    def test_get_author_view(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_data = integrator.get_author_view(author.id, self.build_author())
                self.assertTrue(author_data is not None, "Empty author data")
                self.assertTrue(author_data["posts"] is not None, "No posts returned")
                self.assertTrue(author_data["host"] is not None, "No host is set")
            else:
                self.assertTrue(False, "Unable to find available author")

    def test_send_friend_request(self):
        for integrator in self.integrators:
            foreign_author = self.get_available_author(integrator)
            if foreign_author is not None:
                success = integrator.send_friend_request(self.build_author(), foreign_author)
                self.assertTrue(success, "Friend Request Failed")

    def test_get_authors(self):
        authors = Aggregator.get_authors()
        self.assertTrue(len(authors) > 0, "No authors returned")
