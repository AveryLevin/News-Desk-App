from django.urls import path

from . import views
from django.conf import settings 
from django.conf.urls.static import static

# namespace
app_name = 'news_scraper'

urlpatterns = [
    path('', views.guest_home, name='base'),
    path('register/', views.register_new_user, name='register'),
    path('user_home/', views.user_home, name='user_home'),
    # path('user_home/tags', views.user_tags, name='user_tags'),
    # path('user_home/sources', views.user_sources, name='user_sources'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
]