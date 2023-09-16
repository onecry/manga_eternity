from django.contrib.auth.views import LoginView
from django.urls import path

from .views import UserRegisterView, UserLogoutView

app_name = "userauth"

urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="userauth/login.html",
             redirect_authenticated_user=True
             ),
         name="login"
         ),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout")
]
