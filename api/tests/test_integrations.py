from ..integrations import Integrator, Accumulator
from django.test import TestCase

class IntegrationTests(TestCase):

    def setUp(self):
        self.integrators = Accumulator.get_integrators()

    def test_public_posts(self):
        print "WTF"
        count = 0
        for integrator in self.integrators:
            posts = integrator.get_public_posts()
            count += len(posts)
            self.assertEqual(posts is not None, True, "No posts returned")

        posts = Accumulator.get_public_posts()
        print posts, "POSTS"
        self.assertEquals(len(posts), count, "Different post counts returned")
