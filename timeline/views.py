from django.shortcuts import render
from django.http import Http404
from author.models import User
from author.models import UserDetails
from timeline.models import Post, Comment
from timeline.serializers import PostsSerializer, CommentSerializer

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
        """
        Returns a list of Posts associated with a UserDetail's (User) uuid field.

        See https://docs.djangoproject.com/en/1.7/topics/db/queries/#spanning-multi-valued-relationships
        for information about quering foriegn keys that span multiple objects.
        """
        try:
            return Post.objects.filter(user__userdetails__uuid=uuid)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        posts = self.get_object(uuid)

        serializer = PostsSerializer(posts, many=True)

        # Insert mock external server data into the response
        # No, this is not a good way of doing this and can actually be coded into PostSerializer
        # pl = json.dumps(serializer.data)
        # pl = json.loads(pl)
        # pl += self.get_extern_posts(1)

        return Response(serializer.data)

    def get_extern_posts(self, uuid):
        """Returns a list posts from external nodes"""

        # Pretend that we GET external posts here
        # Will eventually be handled with threading in seperate module.
        # Mock data with a date in the future for testing sorting

        return [{'user':{'username':'jmaguire', 'first_name':'Jerry', 'last_name':'Maguire'}, 'date': '2015-02-25', 'text': u'You complete me', 'image': None, 'id': 99,}]
