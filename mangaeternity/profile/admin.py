from django.contrib import admin
from .models import UserProfile, Manga, UserMangaList

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'email', ]
    list_display = ['__str__', ]
    
@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    fields = ['title', 'manga_id', 'status', ]
    list_display = ['__str__', 'title', 'status', ]
    
@admin.register(UserMangaList)
class UserMangaListAdmin(admin.ModelAdmin):
    fields = ['user_profile', 'manga', ]
    list_display = ['__str__', ]