from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# check if not registered user can see photo list
class PhotoListNotRegisteredUserTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/photoapp/")
        self.assertEqual(response.status_code, 200)


# not registered users can't see 'myphotos'
# he must be redirected to the login page
class MyPhotoListNotRegisteredUserTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/photoapp/photo/mylist/")
        self.assertRedirects(response,"/users/login/?next=/photoapp/photo/mylist/", status_code=302)


# check if it is forbodden to update a photo for not registered users
class PhotoUpdateNotRegisteredUserTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/photoapp/photo/1/update/")
        self.assertEqual(response.status_code, 403)


# registerd user can see but cannot update photo that not his own
class UpdateSomeonesPhotoRegisteredUserTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'randomuser',
            'password': '123password'}
        User.objects.create_user(**self.credentials)
    def test_picture_update(self):
        # send login data
        response = self.client.get("/photoapp/photo/3/update/")
        self.assertEqual(response.status_code, 403)


# upload, update and delete a photo for registered user
class UploadUpdateDeletePhotoRegisteredUserTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': 'secretpass123',
            }
        User.objects.create_user(**self.credentials)
    def test_picture_upload(self):
        User = get_user_model()
        self.client.login(username='test', password='secretpass123')
        response = self.client.get("/photoapp/photo/create/")
        self.assertEqual(response.status_code, 200)


