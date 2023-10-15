from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=320)
    
class Manga(models.Model):
    title = models.CharField(max_length=100)
    manga_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    
class UserMangaList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ManyToManyField(Manga, related_name='read_list')
    def __str__(self):
        return f"{self.user.name}'s reading list"

    @property
    def reading(self):
        return self.manga.filter(status='reading')

    @property
    def plan(self):
        return self.manga.filter(status='plan')

    @property
    def read(self):
        return self.manga.filter(status='read')