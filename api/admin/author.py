from django.contrib import admin
from ..models.author import Author, CachedAuthor


class AuthorOptions(admin.ModelAdmin):
    list_display = ['id', 'user', 'github_username', 'host', 'bio']


class CachedAuthorOptions(admin.ModelAdmin):
    list_display = ['id', 'displayname', 'host', 'url']

    # Deletion should occur only through Author models and friend/followers
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Author, AuthorOptions)
admin.site.register(CachedAuthor, CachedAuthorOptions)
