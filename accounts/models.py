from django.db import models
from django.contrib.auth.models import User

from PIL import Image

class Picture(models.Model):
    pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)


class Preferences(models.Model):
    user = models.OneToOneField(User, related_name='preferences', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    bio = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
