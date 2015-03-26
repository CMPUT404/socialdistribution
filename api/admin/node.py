from django.contrib.admin import ModelAdmin, site

class NodeOptions(ModelAdmin):
    list_display = ['user', 'host', 'enabled', 'api_postfix', 'integrated', 'image_sharing', 'foreign_username']

    def share_images(self, request, queryset):
        try:
            queryset.update(image_sharing=True)
            self.message_user(request, "successfully enabled image sharing")
        except:
            self.message_user(request, "Failed to enable image sharing")
    share_images.short_description = "enable image sharing"

    def dont_share_images(self, request, queryset):
        try:
            queryset.update(image_sharing=False)
            self.message_user(request, "successfully disabled image sharing")
        except:
            self.message_user(request, "Failed to enable image sharing")
    dont_share_images.short_description = "disable image sharing"

    actions = [share_images, dont_share_images]
