from django.contrib.auth.views import LoginView
from django.urls import path

from .views import UserRegisterView, UserLogoutView, MyProfileView

app_name = "profile"

urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="profile/login.html",
             redirect_authenticated_user=True
             ),
         name="login"
         ),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("myprofile/", MyProfileView.as_view(), name="myprofile"),
]
