from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from photoapp.models import Photo


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


# check if registered user can upload an image
class UploadPhotoRegisteredUserTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': 'secretpass123',
            }
        User.objects.create_user(**self.credentials)
    # test if regisrered user can go to "add photo" page
    def test_picture_upload(self):
        self.client.login(username='test', password='secretpass123')
        response = self.client.get("/photoapp/photo/create/")
        self.assertEqual(response.status_code, 200)
    # test if registered user can upload new photo
    def test_create_new_photo(self):
        self.client.login(username='test', password='secretpass123')
        data = {"title": "this is test title",
        "description": "this is test description",
        "image": SimpleUploadedFile(name='photofortest.png',
        content=open("/Users/stash/Desktop/my_projects/not_hotdog/tests/picturefortst.png", 'rb').read(), content_type='image/jpeg')}
        response = self.client.post("/photoapp/photo/create/", data=data)
        self.assertEqual(Photo.objects.count(),1)
        self.assertRedirects(response,"/photoapp/", status_code=302)





 




