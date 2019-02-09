from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404

from hitcount.views import HitCountDetailView

from .models import Post, Place
from .forms import CommentForm


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
    planned_places = Place.objects.filter(status=1)
    visited_places = Place.objects.filter(status=2)
    planned_wedding_places = Place.objects.filter(status=3)
    visited_wedding_places = Place.objects.filter(status=4)
    return render(request, 'blog/map.html',
                  {'planned_places': planned_places,
                   'visited_places': visited_places,
                   'planned_wedding_places': planned_wedding_places,
                   'visited_wedding_places': visited_wedding_places})


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


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'blog/post_view.html'


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_view', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form})


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.post_likes.all():
                obj.post_likes.remove(user)
            else:
                obj.post_likes.add(user)
        return url_


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

