from abc import ABCMeta, abstractproperty
from django.test import TestCase
from .integrations.test_hindlebook import HindlebookIntegration

class IntegrationTests(TestCase):
    __metaclass__ = ABCMeta

    @abstractproperty
    def integrator(self):
        pass

    def setUp(self):
        pass

    def test_public_posts(self):
        print "HERE"
        posts = self.integrator.public_posts()
        self.assertEqual(posts is None, True, "No posts returned")

IntegrationTests.register(HindlebookTests)
