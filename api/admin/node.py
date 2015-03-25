from django.contrib.admin import ModelAdmin

class NodeOptions(ModelAdmin):
    list_display = ['user', 'host', 'enabled', 'api_postfix', 'integrated', 'foreign_username']
