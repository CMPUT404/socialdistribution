from django.contrib.admin import ModelAdmin
from ..models.content import Post, Comment

class PostOptions(ModelAdmin):
    list_display = ['guid', 'author', 'title', 'pubDate', 'content', \
                    'contentType', 'visibility', 'categories', 'image']

class CommentOptions(ModelAdmin):
    list_display = ['guid', 'author', 'pubDate', 'post', 'comment']
