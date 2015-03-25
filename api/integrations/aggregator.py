from ..models import Node
from . import Integrator

class Aggregator(object):

    @staticmethod
    def get_integrators():
        nodes = Node.objects.filter(integrated=True)
        integrators = []
        for node in nodes:
            integrators.append(Integrator(node))

        return integrators

    @staticmethod
    def get_public_posts():
        posts = []
        for integrator in Aggregator.get_integrators():
            node_posts = integrator.get_public_posts()
            posts.extend(node_posts)
        return posts
