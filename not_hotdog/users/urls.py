from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import SignUpView, CustomLoginView, ShowUserNameView


app_name = "user"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"), # custom view
    path("login/", CustomLoginView.as_view(), name="login"), # custom view
    path("logout/", LogoutView.as_view(), name="logout"), # Django built-in logout view
    path("display_users/", login_required(ShowUserNameView.as_view()), name="display_users"), # listing registered users
]

