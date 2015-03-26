from django.contrib.admin import ModelAdmin, BooleanFieldListFilter


class AuthorOptions(ModelAdmin):
    list_display = ['id', 'user', 'github_username', 'host', 'bio', 'enabled']
    list_editable = ['user', 'github_username', 'host', 'bio', 'enabled']
    list_filter = (
        ('enabled', BooleanFieldListFilter),
    )

    def approve_author(self, request, queryset):
        queryset.update(enabled=True)
    approve_author.short_description = "Allow user access the app"

    def disable_author(self, request, queryset):
        queryset.update(enabled=False)
    disable_author.short_description = "Prevent user from accessing the app"

    actions = [approve_author, disable_author]


class CachedAuthorOptions(ModelAdmin):
    list_display = ['id', 'displayname', 'host', 'url']
    list_editable = ['displayname', 'host', 'url']

    # Deletion should occur only through Author models and friend/followers
    def has_delete_permission(self, request, obj=None):
        return False
