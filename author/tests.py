from django.test import TestCase
from django.contrib.auth.models import User

from author.models import UserDetails

import uuid

# Values to be inserted and checked in the Author model
GITHUB_USERNAME = "mraypold"
BIO = "This is my witty biography!"

# Values to be inserted and checked in the User model
# required User model attributes
USERNAME = "raypold"
PASSWORD = uuid.uuid4()

# optional User model attributes
FIRST_NAME = "Michael"
LAST_NAME = "Raypold"
EMAIL = "raypold@ualberta.ca"

class UserDetailsDatabaseTestCase(TestCase):
    """
    Basic testing of the Author model creation and database insertion
    """
    def setUp(self):
        self.user = User.objects.create_user(username = USERNAME,
            first_name = FIRST_NAME,
            last_name = LAST_NAME,
            email = EMAIL,
            password = PASSWORD)

        self.user.save()

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()

    def test_set_up(self):
        """ Assert that that the user model was created in setUp()"""
        try:
            user = User.objects.get(username = USERNAME)
        except:
            self.assertFalse(True, 'Error retrieving %s from database' %USERNAME)

        self.assertEquals(user.first_name, FIRST_NAME)
        self.assertEquals(user.last_name, LAST_NAME)
        self.assertEquals(user.email, EMAIL)

    def test_author_create_insert(self):
        try:
            user_details = UserDetails.objects.create(user = self.user,
                github_username = GITHUB_USERNAME,
                bio = BIO)
        except:
            self.assertFalse(True, 'Author object not created and inserted into db')

    def test_author_delete_by_id(self):
        user_details = UserDetails.objects.create(user = self.user)
        try:
            query = UserDetails.objects.filter(id = user_details.id).delete()
            self.assertEquals(query, None)
        except:
            self.assertFalse(True, 'Author deletion failed')
