from django.shortcuts import render
from django.http import Http404

from author.models import User
from author.models import Author, FriendRelationship

from timeline.models import Post, Comment, ACL
from timeline.serializers import (
    PostSerializer,
    CommentSerializer,
    ACLSerializer )
from timeline.permissions import IsFriend, IsAuthor, Custom

from rest_framework.views import APIView
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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

class CreatePost(APIView):
    """
    Create and returns Post model using an incoming authenticated user

    User is inferred from the Authentication token header

    In JSON:
        {'text':'msg'} is required
        public, fof and image fields are optional.

    Out JSON Data: Full Post model (see PostSerializer)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthor,)

    def post(self, request, format=None):
        data = json.loads(request.body)
        author = Author.objects.get(user = request.user)
        # acl_data = data.get('acl', {"permissions": 300,"shared_users": []})
        # acl = ACL.objects.create(**acl_data)
        serializer = PostSerializer(data = data, context={'author':author})
        # acl_serializer = ACLSerializer(data = request.data['acl'])
        if serializer.is_valid(raise_exception = True):
            post = serializer.create(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class GetDeleteAddComments(APIView):
    """
    This view allows attaching comments to a post
    and deleting comments from a post.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, commentid):
        try:
            comment = Comment.objects.get(id=commentid)
        except:
            raise Http404
        return comment

    def get(self, request, commentid, format=None):
        """
        For testing purposes only.
        Gets an individual comment.
        """
        try:
            comment = self.get_queryset(commentid)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, postid, format=None):
        """
        Adds a comment to a post.
        """
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            author = Author.objects.get(user = request.user)
            post = Post.objects.get(id=postid)
            serializer.save(post = post, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def delete(self, request, commentid, format=None):
        """
        Deletes a comment by id
        """
        try:
            comment = self.get_queryset(commentid)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetPosts(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, Custom,)

    def get_queryset(self, id, postid):
        """
        This view should return a list of all the posts
        for the specified user.
        """
        if postid:
            result = Post.objects.filter(author__id=id, id=postid)
        else:
            result = Post.objects.filter(author__id=id)

        for post in result:
            self.check_object_permissions(self.request, post)
        return result

    def get(self, request, id, postid=None, format=None):
        # return multiple posts
        posts = self.get_queryset(id, postid)
        serializer = PostSerializer(posts, many=True)

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
