from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from . import views

sitemaps = {
    'posts': PostSitemap
}

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    url(r'post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post-detail'),
    url(r'post/(?P<slug>[-\w]+)/like', views.PostLikeToggle.as_view(), name='post-like-toggle'),
    path('map', views.map, name='map'),
    path('about_us', views.about_us, name='about_us'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    url(r'post/(?P<slug>[-\w]+)/comment', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^favicon.ico/$', lambda x: HttpResponseRedirect('static/pictures/favicon..png')),
    url(r'^sitemap\.xml/$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]