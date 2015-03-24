from django.contrib import admin
from ..models import Node, Author, Post, Comment, CachedAuthor
from . import content, author, node

admin.site.register(Node, node.NodeOptions)
admin.site.register(Author, author.AuthorOptions)
admin.site.register(CachedAuthor, author.CachedAuthorOptions)
admin.site.register(Post, content.PostOptions)
admin.site.register(Comment, content.CommentOptions)
