from django.db import models
from django.utils import timezone
from django.urls import reverse
from markdownx.utils import markdownify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCount, HitCountMixin


class Category(models.Model):
    name = models.CharField(max_length=32)
    name_pl = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)
    name_pl = models.CharField(max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    bio = models.TextField(max_length=5000)
    bio_pl = models.TextField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return self.first_name


class Trip(models.Model):
    name = models.CharField(max_length=32)
    name_pl = models.CharField(max_length=32, blank=True, null=True)
    destination = models.CharField(max_length=50)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=32)
    picture = models.ImageField(upload_to='pictures/', blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, blank=True, null=True)
    taken = models.DateTimeField(blank=True, null=True)
    uploaded = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class PlaceStatus(models.Model):
    status = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Place statuses"
    
    def __unicode__(self):
        return self.status

    def __str__(self):
        return self.status


class Place(models.Model):
    name = models.CharField(max_length=32)
    name_pl = models.CharField(max_length=32, blank=True, null=True)
    coord_v = models.FloatField()
    coord_h = models.FloatField()
    status = models.ForeignKey(PlaceStatus, on_delete=models.CASCADE)
    trip = models.ManyToManyField(Trip, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Post(models.Model, HitCountMixin):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    place = models.ManyToManyField(Place, related_name='posts')
    title_place = models.CharField(max_length=100, blank=True, null=True)
    title_place_pl = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    title_pl = models.CharField(max_length=100, unique=True, blank=True, null=True)
    byline = models.CharField(max_length=255)
    byline_pl = models.CharField(max_length=255, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    text = models.TextField()
    text_pl = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=128)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    main_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='main_image')
    images = models.ManyToManyField(Image, related_name='images', blank=True)
    instagram_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    post_likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # Create a property that returns the markdown instead
    @property
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_like_url(self):
        return reverse('post-like-toggle', kwargs={'slug': self.slug})

    def get_api_like_url(self):
        return reverse('post-like-api-toggle', kwargs={'slug': self.slug})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(default="guest", max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
