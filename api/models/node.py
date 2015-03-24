from user import APIUser

# Represents a Node rather than an actual User
class Node(APIUser):
    """
    Extends the existing Django User model as reccomended in the docs.
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/
    """
