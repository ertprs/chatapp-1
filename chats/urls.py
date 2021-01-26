from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('chat/<int:id>', views.chat_message, name='chat_message'),
    path('chat/search_results', views.search_for_friends, name='search_for_friends'),
    path('friends', views.friends, name='friends'),
    path('friends/delete/<int:id>', views.delete_thread, name='delete_friend'),
    path('chat/search_results/<int:id>', views.send_a_friend_request, name='send_a_friend_request'),
    path('friends/accept/<int:id>', views.accept_request, name='accept_request'),
]