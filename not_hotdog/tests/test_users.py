from django.contrib.auth.models import User
from django.test import TestCase


# testing if signup works and redirects you to 'all images' list
class SignUpRedirectTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post('/users/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
        # check if redirected to the photo list page
        self.assertRedirects(response, '/photoapp/', status_code=302)


# not registered user can't see names of other users
# he will be redirected to the login page
class ShowUserNamesNotRegisteredUserTest(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/users/display_users/")
        self.assertRedirects(response,"/users/login/?next=/users/display_users/", status_code=302)