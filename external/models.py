from django.db import models

class Server(models.Model):
    address = models.URLField(blank=False)

class Endpoints(models.Model):
    server = models.ForeignKey('Server')
    url = models.URLField(blank=False)

class RequestType(models.Model):
    # All possible API types go here
    GETFRIENDS = 'GetFriends'
    GETREQUESTS = "GetRequests"
    GETFOLLOWERS = "GetFollowers"

    # Options if using HTML forms.
    RTYPE_CHOICES = (
        (GETFRIENDS, 'Get Friends'),
        (GETREQUESTS, 'Get Friend Requests'),
        (GETFOLLOWERS, 'Get Followers'))

    rtype = models.CharField(max_length = 50, choices=RTYPE_CHOICES)
    endpoint = models.ForeignKey('Endpoints')
