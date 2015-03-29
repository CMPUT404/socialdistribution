from rest_framework.test import APITestCase
from api_settings import settings
from ..integrations import Integrator, Aggregator
from ..models import Node, CachedAuthor
from django.contrib.auth.models import User
import uuid

class IntegrationTests(APITestCase):

    def setUp(self):
        # need to specify nodes here otherwise there won't be anything in the nodes
        # db
        user = User.objects.create(username="hindlebook")
        user.save()
        Node.objects.get_or_create(
            user=user,
            host="http://hindlebook.tamarabyte.com/",
            foreign_username="socshizzle",
            foreign_pass="socshizzle",
            outbound=True
        )
        self.integrators = Aggregator.get_integrators()

    def test_author(self):
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
            return CachedAuthor(
                host="http://localhost:8001/api/",
                # host=data["host"],
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
                author_posts = Aggregator.get_posts_for_authors([author], self.test_author())
                self.assertTrue(type(author_posts) is list, "Expected get_author_posts to return a list")

    def test_get_author_view(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_data = integrator.get_author_view(author.id, self.test_author())
                self.assertTrue(author_data is not None, "Empty author data")
                self.assertTrue(author_data["posts"] is not None, "No posts returned")
                self.assertTrue(author_data["host"] is not None, "No host is set")
            else:
                self.assertTrue(False, "Unable to find available author")

    def test_send_friend_request(self):
        for integrator in self.integrators:
            foreign_author = self.get_available_author(integrator)
            if foreign_author is not None:
                success = integrator.send_friend_request(self.test_author(), foreign_author)
                print success
                self.assertTrue(success, "Friend Request Failed")

    def test_get_authors(self):
        authors = Aggregator.get_authors()
        self.assertTrue(len(authors) > 0, "No authors returned")
