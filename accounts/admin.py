from django.contrib import admin

from .models import Picture, Profile, Preferences

# Register your models here.
admin.site.register(Picture)
admin.site.register(Profile)
admin.site.register(Preferences)