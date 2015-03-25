from ..tests.test_integrations import IntegrationTests
from ...integrations.integrator import Integrator

class HindlebookTests(IntegrationTests):

    integrator = Integrator("http://hindlebook.tamarabyte.com", "test", "test")

    @property
    def integrator(self):
        return self.integrator
