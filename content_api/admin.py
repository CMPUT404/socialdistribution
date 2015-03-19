from django.contrib import admin
from models import Post, Comment

class PostOptions(admin.ModelAdmin):
    list_display = ['guid', 'author', 'pubDate', 'content', 'acl', 'comments']

class CommentOptions(admin.ModelAdmin):
    list_display = ['guid', 'author', 'pubDate', 'post', 'content']

# admin.site.register(Post, PostOptions)
# admin.site.register(Comment, CommentOptions)
