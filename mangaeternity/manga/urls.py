from django.urls import path
from .views import home_page_view, get_manga_name_view, get_titles_view, title_details_view, title_chapters_view, read_chapter_view

app_name = "manga"

urlpatterns = [
    path("", home_page_view, name="home_page"),
    path("search/", get_manga_name_view, name="manga_search"),
    path("titles/", get_titles_view, name="titles_list"),
    path("title/<manga_id>/", title_details_view, name="title_details"),
    path("title/<manga_id>/chapters/", title_chapters_view, name="title_chapters"),
    path("read/<chapter_id>", read_chapter_view, name="read_chapter"),
]
