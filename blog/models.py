from django.db import models
from django.utils import timezone
from django.urls import reverse
from markdownx.utils import markdownify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    bio = models.TextField(max_length=5000)

    def __str__(self):
        return self.first_name


class Trip(models.Model):
    name = models.CharField(max_length=32)
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
    coord_v = models.FloatField()
    coord_h = models.FloatField()
    status = models.ForeignKey(PlaceStatus, on_delete=models.CASCADE)
    trip = models.ManyToManyField(Trip, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    place = models.ManyToManyField(Place, blank=True)
    title = models.CharField(max_length=100, unique=True)
    byline = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag, blank=True)
    text = models.TextField()
    slug = models.SlugField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    main_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='main_image')
    images = models.ManyToManyField(Image, related_name='images', blank=True)
    instagram_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    post_likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_like_url(self):
        return reverse('post-like-toggle', kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse('post-like-api-toggle', kwargs={'pk': self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
