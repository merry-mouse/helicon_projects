from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, CustomLoginView
from . import views


app_name = "user"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"), # custom view
    path("login/", CustomLoginView.as_view(), name="login"), # custom view
    path("logout/", LogoutView.as_view(), name="logout"), # Django built-in logout view
    path("display_users/", views.showusername, name="display_users"),
]

