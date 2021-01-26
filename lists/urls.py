from django.urls import path, re_path
from . import views

urlpatterns = [
    path('new-list', views.start_a_new_list, name='start_a_new_list'),
    path('new-list/<int:id>', views.view_list, name='view_list'),
    path('lists', views.list_view, name='list_view'),
    path('lists/<int:id>', views.list_detail, name='list_detail'),
    path('lists/<int:id>/delete', views.delete_item, name='delete_item'),
    path('lists/delete/<int:id>', views.delete_list, name='delete_list'),
]