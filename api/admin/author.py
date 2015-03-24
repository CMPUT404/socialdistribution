from django.contrib.admin import ModelAdmin


class AuthorOptions(ModelAdmin):
    list_display = ['id', 'user', 'github_username', 'host', 'bio']


class CachedAuthorOptions(ModelAdmin):
    list_display = ['id', 'displayname', 'host', 'url']

    # Deletion should occur only through Author models and friend/followers
    def has_delete_permission(self, request, obj=None):
        return False
