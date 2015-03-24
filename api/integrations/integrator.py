from abc import ABCMeta
from requests.api import request
from requests.auth import HTTPBasicAuth

class Integrator:
    __metaclass__ = ABCMeta

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def build_auth(self, endpoint, data, headers=None):
        return HTTPBasicAuth(self.username, self.password)

    def build_request(self, method, endpoint, data):
        url = self.host + endpoint
        return request(
            url,
            endpoint,
            auth=self.build_auth(),
            data=data,
        )

    def public_posts(self):
        response = self.build_request("get", "/posts")
        return response.json()
