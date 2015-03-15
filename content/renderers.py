from rest_framework.renderers import JSONRenderer

class PostsJSONRenderer(JSONRenderer):
    """
    Modifies the outgoing post listings to conform to the project specifications.

    Base JSONRenderer Response:
        {
          [listing of posts]
        }
    Modified PostsJSONRenderer Response
        {
          posts:[listing of posts]
        }

    This functionality could also be provided by wrapping PostSerializer with
    another serializer class.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'posts': data}
        return super(PostsJSONRenderer, self).render(data, accepted_media_type, renderer_context)
