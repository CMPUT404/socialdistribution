from ..models import Node
from . import Integrator

class Aggregator(object):
    """
    This class handles the intricacies of aggregating data among all registered
    foreign nodes.
    """

    @staticmethod
    def get_integrators():
        """
        Builds integrators for each of our registered nodes if custom logic is
        needed. Should only ever really be used in testing situations outside of
        this class.
        """
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
    def get_posts_for_authors(authors, local_author):
        """Aggregate posts using a list of cached authors"""
        posts = []
        for author in authors:
            integrator = Integrator.build_for_author(author)
            posts.extend(integrator.get_author_posts(author.id, local_author))

        return posts

    @staticmethod
    def get_authors():
        """Fetches all registered authors from all nodes."""
        authors = []
        for integrator in Aggregator.get_integrators():
            node_authors = integrator.get_authors()
            authors.extend(node_authors)

        return authors
