from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name='home-page'),
    # path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # path('profile/<int:id>', views.profile, name='profile'),

    # new
    path('profile', views.my_profile, name='my_profile'),
    path('profile/delete', views.delete_account, name='delete_account'),
    path('profile/settings', views.settings_, name='settings'),
    path('signup', views.signup, name='signup'),

    path('profile/upload', views.upload, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
