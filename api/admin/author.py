from django.contrib.admin import ModelAdmin, BooleanFieldListFilter


class AuthorOptions(ModelAdmin):
    list_display = ['id', 'user', 'github_username', 'host', 'bio', 'enabled','friends','following','requests','pending']
    list_editable = ['user', 'github_username', 'host', 'bio', 'enabled']
    list_filter = (
        ('enabled', BooleanFieldListFilter),
    )

    def approve_author(self, request, queryset):
        try:
            queryset.update(enabled=True)
            self.message_user(request, "Account(s) successfully enabled")
        except:
            self.message_user(request, "Failed to enable account(s)")
    approve_author.short_description = "enable account(s)"

    def disable_author(self, request, queryset):
        try:
            queryset.update(enabled=False)
            self.message_user(request, "Account(s) successfully disabled")
        except:
            self.message_user(request, "Failed to disable account(s)")
    disable_author.short_description = "disable account(s)"

    actions = [approve_author, disable_author]


class CachedAuthorOptions(ModelAdmin):
    list_display = ['id', 'displayname', 'host', 'url']
    list_editable = ['displayname', 'host']

    # Deletion should occur only through Author models and friend/followers
    def has_delete_permission(self, request, obj=None):
        return False
