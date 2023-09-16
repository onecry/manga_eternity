import requests
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, TemplateView, DetailView

from mangaeternity.settings import MANGA_URL, MANGA_IMAGES_URL
from .forms import MangaTitleForm

def get_manga_name_view(request:HttpRequest):
    template_name = 'search/manga_search.html'
    
    if request.method == 'POST':
        form = MangaTitleForm(request.POST)
        if form.is_valid():
            temp_title = form.cleaned_data['title']
            title = temp_title.lower()
            request.session['title'] = title
            return redirect('search:titles_list')
    else:
        form = MangaTitleForm()
        return render(request, template_name, {"form": form})
    
    
def get_titles_view(request:HttpRequest):
    template_name = "search/titles_list.html"
    title = request.session.get('title')
    mangadex_r = requests.get(f"{MANGA_URL}/manga",
        params={"title": title}).json()
    manga_data = mangadex_r["data"]
    
    return render(request, template_name, {"manga_data": manga_data})


def title_details_view(request:HttpRequest, manga_id):
    template_name = "search/title_details.html"
    mangadex_r = requests.get(f"{MANGA_URL}manga/{manga_id}?includes[]=cover_art").json()
    mangadex_data = mangadex_r["data"]
    manga_description = mangadex_data["attributes"]["description"]["en"].replace('---', '**').split('**')[0]
    
    for relationship in mangadex_data["relationships"]:
        if relationship["type"] == "cover_art":
            cover_filename = relationship["attributes"]["fileName"]
    
    return render(request, template_name, {'manga_data': mangadex_data, 'manga_description': manga_description, 'cover_filename': cover_filename})

# def title_read_view(request:HttpRequest, manga_id):
#     template_name = "search/chapter.html"
    
#     mangadex_r = requests.get(
#     f"{MANGA_URL}/manga/{manga_id}/feed",
#     params={"translatedLanguage[]": languages},
#     ).json()
    
#     return render(request, template_name, {"chapers": chapters})
