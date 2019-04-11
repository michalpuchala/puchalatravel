from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from hitcount.views import HitCountDetailView

from .models import Post, Place, Author
from .forms import CommentForm, LanguageChangeForm


def index(request):
    posts = Post.objects.all().order_by('-published_date')
    latest_post = Post.objects.all().order_by('-published_date')[0]
    second_latest_post = Post.objects.all().order_by('-published_date')[1]
    third_latest_post = Post.objects.all().order_by('-published_date')[2]
    latest_post_date = Post.objects.all().order_by('-published_date')[0].published_date.strftime('%d.%m.%Y')
    second_latest_post_date = Post.objects.all().order_by('-published_date')[1].published_date.strftime('%d.%m.%Y')
    third_latest_post_date = Post.objects.all().order_by('-published_date')[2].published_date.strftime('%d.%m.%Y')
    places = Place.objects.all()

    planned_places = Place.objects.filter(status=1)
    visited_places = Place.objects.filter(status=2)
    planned_wedding_places = Place.objects.filter(status=3)
    visited_wedding_places = Place.objects.filter(status=4)

    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'

    response = render(request, 'blog/index.html', {'posts': posts,
                                                   'places': places,
                                                   'latest_post': latest_post,
                                                   'second_latest_post': second_latest_post,
                                                   'third_latest_post': third_latest_post,
                                                   'latest_post_date': latest_post_date,
                                                   'second_latest_post_date': second_latest_post_date,
                                                   'third_latest_post_date': third_latest_post_date,
                                                   'planned_places': planned_places,
                                                   'visited_places': visited_places,
                                                   'planned_wedding_places': planned_wedding_places,
                                                   'visited_wedding_places': visited_wedding_places,
                                                   'LANGUAGE_CODE': language_code
                                                   })

    # Setting language cookie
    if 'LANGUAGE_CODE' not in request.COOKIES:
        response.set_cookie('LANGUAGE_CODE', 'en')
        request.session.set_expiry(3600*24*365)

    return response


def map(request):
    planned_places = Place.objects.filter(status=1)
    visited_places = Place.objects.filter(status=2)
    planned_wedding_places = Place.objects.filter(status=3)
    visited_wedding_places = Place.objects.filter(status=4)

    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'

    return render(request, 'blog/map.html',
                  {'planned_places': planned_places,
                   'visited_places': visited_places,
                   'planned_wedding_places': planned_wedding_places,
                   'visited_wedding_places': visited_wedding_places,
                   'LANGUAGE_CODE': language_code})


def about_us(request):
    magda_bio = Author.objects.filter(id=1)[0]
    michal_bio = Author.objects.filter(id=2)[0]

    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'

    return render(request, 'blog/about_us.html', {'magda_bio': magda_bio,
                                                  'michal_bio': michal_bio,
                                                  'LANGUAGE_CODE': language_code})


def posts(request):
    post_list = Post.objects.all().order_by('-published_date')
    latest_post = Post.objects.all().order_by('-published_date')[0]
    second_latest_post = Post.objects.all().order_by('-published_date')[1]
    third_latest_post = Post.objects.all().order_by('-published_date')[2]
    most_viewed_post = Post.objects.all().order_by('-hit_count_generic__hits')[0]
    second_most_viewed_post = Post.objects.all().order_by('-hit_count_generic__hits')[1]
    third_most_viewed_post = Post.objects.all().order_by('-hit_count_generic__hits')[2]
    latest_post_date = Post.objects.all().order_by('-published_date')[0].published_date.strftime('%d.%m.%Y')
    second_latest_post_date = Post.objects.all().order_by('-published_date')[1].published_date.strftime('%d.%m.%Y')
    third_latest_post_date = Post.objects.all().order_by('-published_date')[2].published_date.strftime('%d.%m.%Y')
    most_viewed_post_date = Post.objects.all().order_by('hit_count_generic__hits')[0].published_date.strftime('%d.%m.%Y')
    second_most_viewed_post_date = Post.objects.all().order_by('hit_count_generic__hits')[1].published_date.strftime('%d.%m.%Y')
    third_most_viewed_post_date = Post.objects.all().order_by('hit_count_generic__hits')[2].published_date.strftime('%d.%m.%Y')

    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'

    return render(request, 'blog/posts.html', {'post_list': post_list,
                                               'latest_post': latest_post,
                                               'second_latest_post': second_latest_post,
                                               'third_latest_post': third_latest_post,
                                               'most_viewed_post': most_viewed_post,
                                               'second_most_viewed_post': second_most_viewed_post,
                                               'third_most_viewed_post': third_most_viewed_post,
                                               'latest_post_date': latest_post_date,
                                               'second_latest_post_date': second_latest_post_date,
                                               'third_latest_post_date': third_latest_post_date,
                                               'most_viewed_post_date': most_viewed_post_date,
                                               'second_most_viewed_post_date': second_most_viewed_post_date,
                                               'third_most_viewed_post_date': third_most_viewed_post_date,
                                               'LANGUAGE_CODE': language_code})


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'blog/post_view.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if 'LANGUAGE_CODE' in self.request.COOKIES:
            language_code = self.request.COOKIES.get('LANGUAGE_CODE')
        else:
            language_code = 'en'
        context['LANGUAGE_CODE'] = language_code
        return context


def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', slug=post.slug)
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form,
                                                                 'LANGUAGE_CODE': language_code})


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.post_likes.all():
                obj.post_likes.remove(user)
            else:
                obj.post_likes.add(user)
        return url_


def signup(request):
    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'
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
    return render(request, 'registration/signup.html', {'form': form,
                                                        'LANGUAGE_CODE': language_code})


def change_language(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':
        form = LanguageChangeForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            if language == 'pl':
                if 'LANGUAGE_CODE' not in request.COOKIES:
                    response.set_cookie('LANGUAGE_CODE', 'pl')
                    request.session.set_expiry(3600 * 24 * 365)
                response.set_cookie('LANGUAGE_CODE', 'pl')
            else:
                if 'LANGUAGE_CODE' not in request.COOKIES:
                    response.set_cookie('LANGUAGE_CODE', 'en')
                    request.session.set_expiry(3600 * 24 * 365)
                response.set_cookie('LANGUAGE_CODE', 'en')

    return response

