from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('chat/<int:id>', consumers.ChatConsumer.as_asgi()),
]
