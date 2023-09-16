from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=320)
    
class Manga(models.Model):
    title = models.CharField(max_length=100)
    manga_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    rating = models.IntegerField()
    
class ReadingList(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    manga = models.ManyToManyField(Manga, related_name='read_list')
    def __str__(self):
        return f"{self.user_profile.name}'s reading list"

    @property
    def read(self):
        return self.manga.filter(status='read')

    @property
    def plan(self):
        return self.manga.filter(status='plan')

    @property
    def i_read(self):
        return self.manga.filter(status='i_read')