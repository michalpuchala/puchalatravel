from django.shortcuts import render
from django.template import RequestContext
from .models import Post, Place


def index(request):
    posts = Post.objects.all().order_by('published_date')
    latest_post = Post.objects.all().order_by('published_date')[0]
    second_latest_post = Post.objects.all().order_by('published_date')[1]
    third_latest_post = Post.objects.all().order_by('published_date')[2]
    return render(request, 'blog/index.html', {'posts': posts,
                                                'latest_post': latest_post,
                                                'second_latest_post': second_latest_post,
                                                'third_latest_post': third_latest_post})

def posts(request):
    return render(request, 'blog/posts.html')

def map(request):
    places = Place.objects.all()
    return render(request, 'blog/map.html', {'places': places})

def about_us(request):
    return render(request, 'blog/about_us.html')
