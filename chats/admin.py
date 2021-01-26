from django.contrib import admin
from .models import FriendRequest, Friend, ChatMessage, ChatThread, SentRequest

# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(Friend)
admin.site.register(ChatMessage)
admin.site.register(ChatThread)
admin.site.register(SentRequest)