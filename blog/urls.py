from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.posts, name='posts'),
    path('map', views.map, name='map'),
    path('about_us', views.about_us, name='about_us'),
]