from rest_framework.test import APITestCase
from api_settings import settings
from ..integrations import Integrator, Aggregator
from ..models import Node, Author, CachedAuthor
from django.contrib.auth.models import User
from ..utils import scaffold
from ..serializers.author import DirtyCachedAuthorSerializer
import uuid

class IntegrationTests(APITestCase):

    def setUp(self):
        user = User.objects.create(username="hindlebook")
        user.save()
        Node.objects.get_or_create(
            user=user,
            # host="http://hindlebook.tamarabyte.com/",
            host="http://localhost:8001/api/",
            foreign_username="test",
            foreign_pass="test",
            outbound=True
        )
        self.integrators = Aggregator.get_integrators()

    def test_author(self):
        id = uuid.uuid4()
        return CachedAuthor(
            id=id,
            host=settings.HOST,
            displayname="Jimmy Bob",
            url= "%sauthor/%s" % (settings.HOST, str(id))
        )

    def test_public_posts(self):
        count = 0
        for integrator in self.integrators:
            posts = integrator.get_public_posts()
            count += len(posts)
            self.assertTrue(isinstance(posts, list), "Expecting posts to be a list")
            self.assertEqual(posts is not None, True, "No posts returned")

        posts = Aggregator.get_public_posts()
        self.assertTrue(isinstance(posts, list), "Expecting posts to be a list")
        self.assertTrue(posts is not None, "posts shouldn't be empty")

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
            return None

    def test_get_author_view(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_data = integrator.get_author_view(author.url, self.test_author())
                print author_data
                self.assertTrue(author_data is not None, "Empty author data")
                self.assertTrue(author_data["posts"] is not None, "No posts returned")
            else:
                self.assertTrue(False, "Unable to find available author")

    def test_get_author_posts(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_posts = integrator.get_author_posts(author.url, author)
                self.assertTrue(len(author_posts) != 0, "Empty author posts")
            else:
                self.assertTrue(False, "Unable to find available author")

    def test_get_posts_for_authors(self):
        for integrator in self.integrators:
            author = self.get_available_author(integrator)
            if author is not None:
                author_posts = Aggregator.get_posts_for_authors([author])
                self.assertTrue(type(author_posts) is list, "Expected get_author_posts to return a list")

    def test_send_friend_request(self):
        for integrator in self.integrators:
            foreign_author = self.get_available_author(integrator)
            if foreign_author is not None:
                success = integrator.send_friend_request(self.test_author(), foreign_author)
                print success
                self.assertTrue(success, "Friend Request Failed")
