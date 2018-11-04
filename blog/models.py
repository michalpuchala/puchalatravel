from django.db import models
from django.utils import timezone
from markdownx.utils import markdownify
from markdownx.models import MarkdownxField


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


class Image(models.Model):
    name = models.CharField(max_length=32)
    picture = models.ImageField(upload_to='pictures/', blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, blank=True, null=True)
    taken = models.DateTimeField(blank=True, null=True)
    uploaded = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name


class PlaceStatus(models.Model):
    status = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Place statuses"
    
    def __unicode__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=32)
    coord_v = models.FloatField()
    coord_h = models.FloatField()
    status = models.ForeignKey(PlaceStatus, on_delete=models.CASCADE)
    trip = models.ManyToManyField(Trip, blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    place = models.ManyToManyField(Place, blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    byline = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    text = MarkdownxField()
    slug = models.SlugField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    main_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='main_image')
    images = models.ManyToManyField(Image, related_name='images', blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
