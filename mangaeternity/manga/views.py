import requests
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from mangaeternity.settings import MANGA_URL
from .forms import MangaTitleForm
from profile.forms import MangaListForm
from profile.models import Manga, UserProfile

def home_page_redirect_view(request:HttpRequest):
    return HttpResponseRedirect("manga")

def home_page_view(request:HttpRequest):
    template_name = 'manga/homepage.html'
    
    order = {
        "rating": "desc",
    }   

    final_order_query = {}

    for key, value in order.items():
        final_order_query[f"order[{key}]"] = value
    
    mangadex_r = requests.get(
        f"{MANGA_URL}/manga?limit=100&includes[]=cover_art&availableTranslatedLanguage%5B%5D=ru&availableTranslatedLanguage%5B%5D=en",
        params={**final_order_query,}
        ).json()
    mangadex_data = mangadex_r["data"]
    
    return render(request, template_name, {"manga_data": mangadex_data})


def get_manga_name_view(request:HttpRequest):
    template_name = 'manga/manga_search.html'
    
    if request.method == 'POST':
        form = MangaTitleForm(request.POST)
        if form.is_valid():
            temp_title = form.cleaned_data['title']
            title = temp_title.lower()
            request.session['title'] = title
            return redirect('manga:titles_list')
    else:
        form = MangaTitleForm()
        return render(request, template_name, {"form": form})
    
    
def get_titles_view(request:HttpRequest):
    template_name = "manga/titles_list.html"
    title = request.session.get('title')
    mangadex_r = requests.get(f"{MANGA_URL}/manga?includes[]=cover_art",
        params={"title": title}).json()
    mangadex_data = mangadex_r["data"]
    
    return render(request, template_name, {"manga_data": mangadex_data})


def title_details_view(request:HttpRequest, manga_id):
    template_name = "manga/title_details.html"
    form = MangaListForm()
    mangadex_r = requests.get(f"{MANGA_URL}/manga/{manga_id}?includes[]=cover_art").json()
    mangadex_data = mangadex_r["data"]
    manga_description = mangadex_data["attributes"]["description"]["en"].replace('---', '**').split('**')[0]
    
    for relationship in mangadex_data["relationships"]:
        if relationship["type"] == "cover_art":
            cover_filename = relationship["attributes"]["fileName"]
            
    if request.user.is_authenticated:
        if not Manga.objects.filter(title=mangadex_data['attributes']['title']['en'], manga_id=manga_id).exists():
            manga = Manga.objects.create(title=mangadex_data['attributes']['title']['en'], manga_id=manga_id)
        return render(request, template_name, {
            'manga_data': mangadex_data, 'manga_description': manga_description,
            'cover_filename': cover_filename,'form':form,
            })
    else:
        return render(request, template_name, {
            'manga_data': mangadex_data, 'manga_description': manga_description, 
            'cover_filename': cover_filename,
            })

def title_chapters_view(request:HttpRequest, manga_id, language):
    template_name = "manga/title_chapters.html"
    languages = [language]
    request.session['language'] = language
    
    mangadex_r = requests.get(
    f"{MANGA_URL}/manga/{manga_id}/feed?limit=500&order%5Bchapter%5D=asc",
    params={"translatedLanguage[]": languages},
    ).json()
    mangadex_data = mangadex_r["data"]
    
    return render(request, template_name, {'manga_data': mangadex_data, 'manga_id': manga_id})

def read_chapter_view(request:HttpRequest, chapter_id, manga_id, next_chapter_id=None):
    template_name = "manga/chapter.html"
    mangadex_r = requests.get(f"{MANGA_URL}/at-home/server/{chapter_id}").json()
    
    # for next chapter
    languages = [request.session['language']]
    
    chapters_r = requests.get(
    f"{MANGA_URL}/manga/{manga_id}/feed?limit=500&order%5Bchapter%5D=asc",
    params={"translatedLanguage[]": languages},
    ).json()
    all_chapters = chapters_r["data"]
    
    for chapters in all_chapters:
        if chapter_id == chapters['id']:
            chapter_index = all_chapters.index(chapters)
            next_chapter_index = chapter_index + 1
            next_chapter_id = all_chapters[next_chapter_index]['id']
    
    return render(request, template_name, {
        'chapter_data': mangadex_r, 'manga_id': manga_id,
        'next_chapter_id': next_chapter_id
        })
