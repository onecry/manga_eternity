from django.urls import path
from .views import get_manga_name_view, get_titles_view, title_details_view

app_name = "search"

urlpatterns = [
    path('search/', get_manga_name_view, name='manga_search'),
    path('search/titles/', get_titles_view, name='titles_list'),
    path('seatch/titles/<manga_id>/', title_details_view, name='title_details')
]
