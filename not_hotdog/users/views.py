from django.views.generic import CreateView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm # to create a new user
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render



# to allow the user to register through the site
class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('photo:list')

    # log in the users before redirecting them to the photo dashboard
    def form_valid(self,form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)
        return to_return


class CustomLoginView(LoginView):
    template_name = "users/login.html"



class ShowUserNameView(ListView):
    model = User
    template_name = 'users/display_users.html'
    context_object_name = 'usernames'