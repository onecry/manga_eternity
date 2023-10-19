from django.db import models
from django.contrib.auth.models import User
    
class Manga(models.Model):
    title = models.CharField(max_length=100)
    manga_id = models.CharField(max_length=100)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=320)
    manga = models.ManyToManyField(Manga, related_name='user_manga')
    reading = models.ManyToManyField(Manga, related_name='reading_manga')
    planned = models.ManyToManyField(Manga, related_name='planned_manga')
    read = models.ManyToManyField(Manga, related_name='read_manga')