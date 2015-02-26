from django.shortcuts import render
from django.http import Http404
from author.models import User
from author.models import UserDetails
from timeline.models import Post, Comment
from timeline.serializers import PostSerializer, CommentSerializer

from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.response import Response

import json

class MultipleFieldLookupMixin(object):
    """Allows the lookup of multiple fields in an url for mixins"""
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)

# This method is simple, but its going to present a problem when adding external
# data to our json response
# class GetPosts(MultipleFieldLookupMixin, generics.ListAPIView):
#     queryset = Post.objects.all()
#
#     # Before sending data back we add external server data to the queryset here
#     # http://stackoverflow.com/questions/13603027/django-rest-framework-non-model-serializer
#
#     serializer_class = PostSerializer
#     lookup_fields = ('author')

class GetPosts(APIView):
    def get_object(self, uuid):
        try:
            # return Post.objects.all().filter(author = aid)
            # convert from uuid to user
            user = User.objects.filter(userdetails__uuid=uuid)[0]
            return Post.objects.filter(user=user)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        post = self.get_object(uuid)
        # serializer = PostSerializer(posts, many=True)
        serializer = PostSerializer(post)
        # Insert mock external server data into the response
        # No, this is not a good way of doing this and can actually be coded into PostSerializer
        # pl = json.dumps(serializer.data)
        # pl = json.loads(pl)
        # pl += self.get_extern_posts(1)

        return Response(serializer.data)

    def get_extern_posts(self, uuid):
        """Returns a list posts from external nodes"""

        # Pretend that we GET external posts here
        # Mock data with a date in the future for testing sorting

        return [{'user': 1, 'date': '2015-02-25', 'text': u'Some other text', 'image': None, 'id': 99, 'acl': None}]
