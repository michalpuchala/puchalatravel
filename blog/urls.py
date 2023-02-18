from django.urls import path, include, re_path
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
    re_path(r'post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post-detail'),
    re_path(r'post/(?P<slug>[-\w]+)/like', views.PostLikeToggle.as_view(), name='post-like-toggle'),
    path('map', views.map, name='map'),
    path('about_us', views.about_us, name='about_us'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    re_path(r'post/(?P<slug>[-\w]+)/comment', views.add_comment_to_post, name='add_comment_to_post'),
    re_path(r'^favicon.ico/$', lambda x: HttpResponseRedirect('static/pictures/favicon..png')),
    re_path(r'^sitemap\.xml/$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    re_path(r'^change_language$', views.change_language, name='change_language')
]