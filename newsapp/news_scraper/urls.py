from django.urls import path

from . import views
from django.conf import settings 
from django.conf.urls.static import static

# namespace
app_name = 'news_scraper'

urlpatterns = [
    path('register/', views.register_new_user, name='register'),
    path('<str:user_name>/', views.user_home, name='user_home')
]