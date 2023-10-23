from typing import Any
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView

from .forms import CustomUserCreationForm
from .models import UserProfile

#Auth views

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('manga:homepage.html')

        return render(request, 'profile/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('manga:homepage.html')

    return render(request, 'profile/login.html', {"error": "Invalid login credentials"})

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("profile:login")

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "profile/register.html"
    success_url = reverse_lazy("manga:homepage")

    def form_valid(self, form):
        response = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")
        user = authenticate(self.request, username=username, password=password, email=email)
        login(request=self.request, user=user)


        return response
    
#Profile views
    
class MyProfileView(TemplateView):
    template_name = "profile/myprofile.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        return context