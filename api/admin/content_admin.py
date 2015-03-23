from django.contrib import admin
from models import Post, Comment

class PostOptions(admin.ModelAdmin):
    list_display = ['guid', 'author', 'title', 'pubDate', 'content', \
                    'contentType', 'visibility', 'categories', 'image']

class CommentOptions(admin.ModelAdmin):
    list_display = ['guid', 'author', 'pubDate', 'post', 'comment']

admin.site.register(Post, PostOptions)
admin.site.register(Comment, CommentOptions)
