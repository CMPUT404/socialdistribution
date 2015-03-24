from django.contrib import admin
from ..models.node import Node

class NodeOptions(admin.ModelAdmin):
    list_display = ['id', 'host', 'enabled']

admin.site.register(Node, NodeOptions)
