from user import APIUser
from django.db.models import fields

class Node(APIUser):
    foreign_username = fields.CharField(max_length=32)
    foreign_pass = fields.CharField(max_length=32)
    outbound = fields.BooleanField(default=False)
    image_sharing = fields.BooleanField(default=True)

    # Used to set parent "type" to "Node"
    def __init__(self, *args, **kwargs):
        for f in self._meta.fields:
            if f.attname == "type":
                f.default = "Node"
                super(Node, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return u'%s:%s' % (self.id, self.host)
