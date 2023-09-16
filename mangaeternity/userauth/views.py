from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView

from .forms import CustomUserCreationForm
from .models import UserProfile

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('search:manga_search.html')

        return render(request, 'userauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('search:manga_search.html')

    return render(request, 'userauth/login.html', {"error": "Invalid login credentials"})

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("userauth:login")

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "userauth/register.html"
    success_url = reverse_lazy("search:manga_search")

    def form_valid(self, form):
        response = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")
        user = authenticate(self.request, username=username, password=password, email=email)
        login(request=self.request, user=user)


        return response
    
