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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.http import JsonResponse

import json

class TimelineBuilder():
    """
    Builds a timeline from a queryset
    """

    page_size = 20

    def __init__(self, queryset=None):
        self.posts = []

        if queryset:
            self.add_queryset(queryset)

    def add_queryset(self, queryset):
        for post in queryset:
            self.posts.append(PostSerializer(post).data)

    # TODO retuns all posts right now
    # Divide self.posts into equal pages based on page_size
    def get_page(self, page = 1):
        return self.posts

    def count(self):
        return len(self.posts)

    def get_timeline(self):
        return {"posts":self.posts}

    def get_posts(self):
        return self.posts

    def __str__(self):
        return unicode(self.get_json())

class GetTimeline(APIView):
    """
    Returns the combination of posts by an author and their friends

    Return JSON:
    {
        posts: [
            {
                id:1
                text:text here
                text:Awesome post,
                date:1425945600,
                image:null,
                author:{displayname:bob,
                    id:020210103310,
                    url:"example.org"
                    last_name:smith }
                comments: [],
                acl: {permissions:200, shared_users: []}
            },
            ...
        ]
    }

    """

    # TODO Implementation Notes:
    # This is horribly inefficient right now and will be improved as time permits.
    # Pagination will come in another milestone

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        timeline = TimelineBuilder()

        timeline.add_queryset(Post.objects.filter(author = request.user))

        # Get friend posts and add to TimelineBuilder
        friends = FriendRelationship.objects.filter(friend = request.user)\
            .values('friendor')

        for friendor in friends:
            timeline.add_queryset(Post.objects.filter(author__id = friendor['friendor']))

        timeline.add_queryset(Post.objects.exclude(author__id__in = friends)
            .exclude(author__id = request.user.id))

        return JsonResponse(timeline.get_timeline(), safe=False)

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
