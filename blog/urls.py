from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like', views.PostLikeToggle.as_view(), name='post-like-toggle'),
    path('api/posts/<int:pk>/like', views.PostLikeAPIToggle.as_view(), name='post-like-api-toggle'),
    path('map', views.map, name='map'),
    path('about_us', views.about_us, name='about_us'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
]