from django.contrib.admin import ModelAdmin

class NodeOptions(ModelAdmin):
    list_display = ['id', 'user', 'host', 'enabled']
