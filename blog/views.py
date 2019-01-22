from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, F
from .models import Post, Place


def index(request):
    posts = Post.objects.all().order_by('published_date')
    latest_post = Post.objects.all().order_by('published_date')[0]
    second_latest_post = Post.objects.all().order_by('published_date')[1]
    third_latest_post = Post.objects.all().order_by('published_date')[2]
    places = Place.objects.all()
    return render(request, 'blog/index.html', {'posts': posts,
                                               'places': places,
                                               'latest_post': latest_post,
                                               'second_latest_post': second_latest_post,
                                               'third_latest_post': third_latest_post})


def map(request):
    places = Place.objects.all()
    return render(request, 'blog/map.html', {'places': places})


def about_us(request):
    return render(request, 'blog/about_us.html')


def posts(request):
    posts = Post.objects.all().order_by('published_date')
    latest_post = Post.objects.all().order_by('published_date')[0]
    second_latest_post = Post.objects.all().order_by('published_date')[1]
    third_latest_post = Post.objects.all().order_by('published_date')[2]
    return render(request, 'blog/posts.html', {'posts': posts,
                                                'latest_post': latest_post,
                                                'second_latest_post': second_latest_post,
                                                'third_latest_post': third_latest_post})


class PostDetailView(generic.DetailView):
    model = Post
    likes = Post.objects.annotate(number_of_likes=Count('post_likes'))
    # Post.objects.filter(id__in=posts).update(post_views=F('vote') + 1)
    template_name = 'blog/post_view.html'


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

