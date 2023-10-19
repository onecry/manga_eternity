from django.db import models
from django.contrib.auth.models import User
    
class Manga(models.Model):
    title = models.CharField(max_length=100)
    manga_id = models.CharField(max_length=100)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=320)
    manga = models.ManyToManyField(Manga, related_name='users')
    reading = models.ManyToManyField(Manga, related_name='reading_users')
    planned = models.ManyToManyField(Manga, related_name='planned_users')
    read = models.ManyToManyField(Manga, related_name='read_users')