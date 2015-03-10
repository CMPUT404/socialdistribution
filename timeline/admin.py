from django.contrib import admin
from models import Post, Comment

class PostOptions(admin.ModelAdmin):
    list_display = ['id', 'author', 'date', 'text', 'acl', 'comments']

class CommentOptions(admin.ModelAdmin):
    list_display = ['id', 'author', 'date', 'post', 'text']

admin.site.register(Post, PostOptions)
admin.site.register(Comment, CommentOptions)
