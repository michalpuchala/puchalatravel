from django import forms
from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget
from django.forms import TextInput, Textarea
from blog.models import Category, Tag, Author, Trip, Image, PlaceStatus, Place, Post

# Adjusting views


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

    fieldsets = [
        (None,      {'fields': ['author', 'trip', 'tag', 'category', 'post_likes']}),
        ('Content', {'fields': ['title', 'byline', 'text']}),
        ('Images',  {'fields': ['main_image', 'images']}),
        ('Dates',   {'fields': ['created_date', 'published_date']}),
        ('Links',   {'fields': ['instagram_link', 'twitter_link', 'slug']}),
    ]


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    def trip_name(self, obj):
        return obj.trip.name
    trip_name.name = 'Name'
    trip_name.admin_order_field = 'trip__name'

    list_display = ('name', 'trip_name', 'uploaded', 'taken')

    fieldsets = [
        (None,    {'fields': ['name', 'picture', 'trip']}),
        ('Dates', {'fields': ['taken', 'uploaded']}),
    ]


class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'start_date', 'end_date')

    fieldsets = [
        (None,    {'fields': ['name', 'destination']}),
        ('Dates', {'fields': ['start_date', 'end_date']}),
    ]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PlaceStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status',)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'bio')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 60})},
    }

    inlines = [
        PostInline,
    ]


# Registering

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PlaceStatus, PlaceStatusAdmin)
admin.site.register(Place, PlaceAdmin)