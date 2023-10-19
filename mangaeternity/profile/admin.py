from django.contrib import admin
from .models import UserProfile, Manga

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'email', 'reading', 'planned', 'read', ]
    list_display = ['__str__', ]
    
@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    fields = ['title', 'manga_id', ]
    list_display = ['__str__', 'title', ]