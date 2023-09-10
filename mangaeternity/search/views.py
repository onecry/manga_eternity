import requests
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, TemplateView, DetailView

from mangaeternity.settings import MANGA_URL
from .forms import MangaTitleForm

def get_manga_name_view(request:HttpRequest):
    template_name = 'search/manga_search.html'
    
    if request.method == 'POST':
        form = MangaTitleForm(request.POST)
        if form.is_valid():
            temp_title = form.cleaned_data['title']
            title = temp_title.lower().replace(' ', '+')
            request.session['title'] = title
            return redirect('search:titles_list')
    else:
        form = MangaTitleForm()
        return render(request, template_name, {"form": form})
    
    
def get_titles_view(request:HttpRequest):
    template_name = "search/titles_list.html"
    title = request.session.get('title')
    
    mangadex_r = requests.get(f"{MANGA_URL}{title}").json()
    
    manga_data = mangadex_r["results"]
        
    return render(request, template_name, {"manga_data": manga_data})


def title_details_view(request:HttpRequest, manga_id):
    template_name = "search/title_details.html"
    
    mangadex_r = requests.get(f"{MANGA_URL}info/{manga_id}").json()
    
    #did this because sometimes description ends with '---' or '**' and after thah symbols was manga awards or links to author
    manga_description = mangadex_r["description"]["en"].replace('---', '**').split('**')[0]
    
    return render(request, template_name, {"manga_data": mangadex_r, 'manga_description': manga_description})

def manga_chapters_view(request:HttpRequest, manga_id):
    pass
