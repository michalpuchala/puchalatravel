from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponseRedirect
from . import views
from puchalatravel.settings.prod import STATIC_URL

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like', views.PostLikeToggle.as_view(), name='post-like-toggle'),
    path('map', views.map, name='map'),
    path('about_us', views.about_us, name='about_us'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('posts/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^favicon.ico/$', lambda x: HttpResponseRedirect('static/pictures/favicon..png')), # google chrome favicon fix
]