from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    bio = models.CharField(max_length=5000)

    def __str__(self):
        return self.first_name


class Trip(models.Model):
    name = models.CharField(max_length=32)
    destination = models.CharField(max_length=50)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=32)
    picture = models.ImageField(default='defualt.png')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    taken = models.DateTimeField(blank=True, null=True)
    uploaded = models.DateTimeField(default=timezone.now)
    width = models.IntegerField()
    height = models.IntegerField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    byline = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag)
    text = models.TextField()
    slug = models.SlugField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    main_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='main_image')
    images = models.ManyToManyField(Image, related_name='images')
    instagram_link = models.URLField()
    twitter_link = models.URLField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
