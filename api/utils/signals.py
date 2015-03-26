from django.db.models.signals import post_save, post_delete

from ..models.author import Author, CachedAuthor

#
# Handles signals relating to the Author and CachedAuthor models
#
# Specifically:
#   1. Preventing updating anomalies between Author/CachedAuthor
#
# Further Extension:
#   1. Signals for friends/followers/following to frontend
#


def update_cached_author(sender, instance, *args, **kwargs):
    """
    Updates a CachedAuthor model with the changes made to Author model

    In general this could be prevented if follower/friend relationships
    had generic m2m relations, but it makes serialization and the views
    significantly more complex. Tradeoff is performance.
    """
    try:
        cached = CachedAuthor.objects.get(id=instance.id)
    except:
        # CachedAuthor has not been created yet. Create it.
        _cached = CachedAuthor(
                              id=instance.id,
                              host=instance.host,
                              url=instance.url,
                              displayname=instance.user.username)
        _cached.save()
        return

    cached.host = instance.host
    cached.displayname = instance.user.username
    cached.save()

def delete_cached_author(sender, instance, *args, **kwargs):
    """
    Delete a CachedAuthor model after deletion of an Author model
    """
    try:
        CachedAuthor.objects.get(id=instance.id).delete()
    except:
        pass

post_save.connect(update_cached_author, sender=Author)
post_delete.connect(delete_cached_author, sender=Author)
