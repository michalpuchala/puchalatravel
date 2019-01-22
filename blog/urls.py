from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('map', views.map, name='map'),
    path('about_us', views.about_us, name='about_us'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
]