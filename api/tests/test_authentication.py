from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.db import transaction
from django.db import IntegrityError
from ..models.author import Author
from api.utils import scaffold
import os
import uuid
import json

# Values to be inserted and checked in the Author model
GITHUB_USERNAME = "jmaguire"
BIO = "I'm the best sports agent around!"
HOST = "http://examples.com/"

# Values to be inserted and checked in the User model
# required User model attributes
RUSERNAME = "jmaquire2"
USERNAME = "jmaguire"
PASSWORD = str(uuid.uuid4())

# optional User model attributes
FIRST_NAME = "Jerry"
LAST_NAME = "Maguire"
EMAIL = "jmaguire@smi.com"

class AuthorAuthentication(APITestCase):
    """
    Basic testing of the Author model creation and database insertion
    """
    def setUp(self):
        self.user_dict = {
            'username':USERNAME,
            'displayname':USERNAME,
            'first_name':FIRST_NAME,
            'last_name':LAST_NAME,
            'password':PASSWORD,
            'email':EMAIL,
            'github_username':GITHUB_USERNAME,
            'bio':BIO,
            'host': HOST }

        self.user_dict_with_img = {
            'username':USERNAME,
            'displayname':USERNAME,
            'first_name':FIRST_NAME,
            'last_name':LAST_NAME,
            'password':PASSWORD,
            'email':EMAIL,
            'github_username':GITHUB_USERNAME,
            'bio':BIO,
            'host': HOST,
            'image': "data:image/jpeg;base64," + scaffold.get_test_image() }

        self.login_dict = {
            'username':USERNAME,
            'password':PASSWORD }

        # Create an already registered user for testing
        self.registed_user = {
            'username':RUSERNAME,
            'password':PASSWORD,
            'first_name':FIRST_NAME,
            'email':EMAIL,
            'last_name':LAST_NAME }

        self.user = User.objects.create_user(**self.registed_user)
        self.author = Author.objects.create(
            user = self.user,
            github_username = GITHUB_USERNAME,
            bio = BIO,
            host = HOST )

        # Use for non authenticated requests
        self.c = scaffold.SocialAPIClient()

        self.basic_client = scaffold.SocialAPIClient()
        self.basic_client.basic_credentials(RUSERNAME, PASSWORD)
        #enable registered user
        scaffold.enable_author(RUSERNAME)

        self.token_client = scaffold.SocialAPIClient()
        self.token_client.token_credentials(self.author)

        self.bad_auth_client = scaffold.SocialAPIClient()
        self.bad_auth_client.bad_credentials(True)

    def tearDown(self):
        """Remove all created objects from mock database"""
        Author.objects.all().delete()
        User.objects.all().delete()
        self.basic_client.credentials()
        self.token_client.credentials()
        self.bad_auth_client.credentials()

    def test_registration(self):
        """
        Test a registration where all values are given in the JSON body
        """
        response = self.c.post('/author/registration', self.user_dict)

        self.assertEquals(response.status_code, 201, "User and Author not created")

        # Confirm that model and all attributes were inserted
        user = User.objects.get(username = USERNAME)
        self.assertEquals(user.username, USERNAME, "Usernames don't match")
        self.assertEquals(user.first_name, FIRST_NAME, "Name doesn't match")
        self.assertEquals(user.last_name, LAST_NAME, "Name doesn't match")

        details = Author.objects.get(user = user)
        self.assertEquals(details.bio, BIO, "Bio doesn't match")
        self.assertEquals(details.github_username, GITHUB_USERNAME, "Username doesn't match")

    def test_registration_with_image(self):
        response = self.c.post('/author/registration', self.user_dict_with_img, format='multipart')
        self.assertEquals(response.status_code, 201)

        # Get image.
        url = response.data.get('author').get('image')
        response = self.c.get(url)
        self.assertEquals(response.status_code, 200)

        scaffold.clean_up_imgs('profile', url)

    def test_registration_same_user(self):
        """
        Test registering duplicate users
        """
        try:
            with transaction.atomic():
                response = self.c.post('/author/registration', self.user_dict)
                self.assertEquals(response.status_code, 201)

                response = self.c.post('/author/registration', self.user_dict)
                self.assertEquals(response.status_code, 400)
            self.assertTrue(True, 'Duplicate users not allowed')
        except IntegrityError:
            pass

    def test_registration_without_username(self):
        self.user_dict.pop('displayname', None)
        response = self.c.post('/author/registration', self.user_dict)

        self.assertEquals(response.status_code, 400, "User should not be created")

    def test_registration_without_email(self):
        self.user_dict.pop('email', None)
        response = self.c.post('/author/registration', self.user_dict)

        self.assertEquals(response.status_code, 201, "User should be created")
        scaffold.assertUserExists(self, response.data['author']['displayname'])

    def test_registration_without_name(self):
        self.user_dict.pop('first_name', None)
        response = self.c.post('/author/registration', self.user_dict)

        self.assertEquals(response.status_code, 201, "User should be created")
        scaffold.assertUserExists(self, response.data['author']['displayname'])

    def test_registration_without_github(self):
        self.user_dict.pop('github_username', None)
        response = self.c.post('/author/registration', self.user_dict)

        self.assertEquals(response.status_code, 201, "User should be created")
        scaffold.assertUserExists(self, response.data['author']['displayname'])

    def test_login_unapproved_user(self):
        """
        Test a registration where all values are given in the JSON body
        """
        response = self.c.post('/author/registration', self.user_dict)

        self.assertEquals(response.status_code, 201, "User and Author not created")

        # Confirm that model matches
        user = User.objects.get(username = USERNAME)
        self.assertEquals(user.username, USERNAME, "Usernames don't match")

        self.c.basic_credentials(self.user_dict['username'], self.user_dict['password'])
        response = self.c.get('/author/login')
        self.assertEquals(response.status_code, 403, 'user should not be allowed to log in')
        # content = json.loads(response.content)

    def test_login(self):
        response = self.basic_client.get('/author/login')
        content = json.loads(response.content)
        print(content)
        self.assertIsNot(content['token'], '', 'Empty Token')
        self.assertIsNotNone(content['token'], 'Empty Token')

        profile = content['author']
        self.assertEquals(profile.has_key('host'), True, "Host key doesn't exist")

        keys = set(profile.keys()).intersection(self.user_dict.keys());
        # Can't test for host since it will be auto-created
        keys.remove('host')

        self.user_dict['displayname'] = RUSERNAME

        for key in keys:
            self.assertEquals(profile[key], self.user_dict[key])

        self.assertEquals(response.status_code, 200, 'user not logged in')

    def test_bad_login(self):
        response = self.bad_auth_client.get('/author/login')
        self.assertEquals(response.status_code, 401, 'user not logged in')

    def test_logout(self):
        response = self.basic_client.post('/author/logout')

        self.assertEquals(response.status_code, 200, "User not logged out")

    def test_author_update(self):
        # All fields are good and should return 200
        update_author_dict = {
            'first_name':FIRST_NAME + "u",
            'last_name':LAST_NAME + "u",
            'email':EMAIL + "u",
            'github_username':GITHUB_USERNAME + "u",
            'bio':BIO + "u",
            'image': "data:image/jpeg;base64," + scaffold.get_test_image() }

        response = self.token_client.post('/author/profile', update_author_dict, format='multipart')
        self.assertEquals(response.status_code, 200)

        # Get image.
        url = response.data.get('image')
        response = self.c.get(url)
        self.assertEquals(response.status_code, 200)
        # scaffold.pretty_print(response.data)

        # Compare the response content to that content in the database
        user = User.objects.get(username = RUSERNAME)
        details = Author.objects.get(user = user)

        self.assertEquals(user.email, update_author_dict['email'])
        self.assertEquals(user.first_name, update_author_dict['first_name'])
        self.assertEquals(user.last_name, update_author_dict['last_name'])

        self.assertEquals(details.bio, update_author_dict['bio'])
        self.assertEquals(details.github_username, update_author_dict['github_username'])

        # Clean up
        scaffold.clean_up_imgs('profile', url)

    def test_author_update_bad_authorization(self):
        old = User.objects.get(username = RUSERNAME)

        update_author_dict = {
            'email':EMAIL + "u",
            'bio':BIO + "u" }

        response = self.bad_auth_client.post('/author/profile', update_author_dict)
        self.assertEquals(response.status_code, 401)

        new = User.objects.get(last_name = LAST_NAME)
        self.assertEquals(old, new, "Author profile should not have been updated")

    def test_author_update_partial(self):
        # All fields are good and should return 200
        update_author_dict = {
            'email':EMAIL + "u",
            'bio':BIO + "u" }

        response = self.token_client.post('/author/profile', update_author_dict)
        self.assertEquals(response.status_code, 200)

        # scaffold.pretty_print(response.data)

        # Compare the response content to that content in the database
        user = User.objects.get(username = RUSERNAME)
        details = Author.objects.get(user = user)

        self.assertEquals(user.email, update_author_dict['email'])
        self.assertEquals(details.bio, update_author_dict['bio'])

    def test_author_update_bad_fields(self):
        """Good fields will still be parsed; bad fields ignored"""
        # All fields are good and should return 200
        update_author_dict = {
            'bad_email':EMAIL + "u",
            'bio':BIO + "u" }

        response = self.token_client.post('/author/profile', update_author_dict)
        self.assertEquals(response.status_code, 200)

        # Compare the response content to that content in the database
        user = User.objects.get(username = RUSERNAME)
        details = Author.objects.get(user = user)

        self.assertTrue(user.email != update_author_dict['bad_email'])
        self.assertEquals(details.bio, update_author_dict['bio'])
