from django.contrib import admin
from models import Author, CachedAuthor


def get_fields(model):
    """Returns a list of model fields that do not contain _id

    Takes a django model instance.
    Fields containing _id are not representable in the admin interface.

    Django returns fields in alpabetical order, so list is alphabetized.
    """
    return filter(lambda field: not field.endswith('_id'),
                  model._meta.get_all_field_names())


class AuthorOptions(admin.ModelAdmin):
    list_display = ['id', 'user', 'github_username', 'host', 'bio']


admin.site.register(Author, AuthorOptions)
admin.site.register(CachedAuthor)
