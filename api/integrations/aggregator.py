from ..models import Node
from . import Integrator

class Aggregator(object):

    @staticmethod
    def get_integrators():
        nodes = Node.objects.filter(outbound=True)
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

    @staticmethod
    # aggregate posts using a list of cached authors
    def get_posts_for_authors(authors, local_author):
        posts = []
        for author in authors:
            integrator = Integrator.build_for_author(author)
            posts.extend(integrator.get_author_posts(author.id, local_author))

        return posts

    @staticmethod
    # Fetches all available authors from all nodes
    def get_authors():
        authors = []
        for integrator in Aggregator.get_integrators():
            node_authors = integrator.get_authors()
            authors.extend(node_authors)

        return authors
