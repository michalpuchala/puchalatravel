from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from blog.models import Category, Tag, Author, Trip, Image, PlaceStatus, Place, Post, Comment


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class PostsInLine(admin.TabularInline):
    model = Post.place.through
    extra = 1


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 40, 'cols': 100})},
    }

    fieldsets = [
        (None,      {'fields': ['slug', 'published', 'author', 'trip', 'tag', 'category', 'place', 'title_place', 'title_place_pl']}),
        ('Content', {'fields': ['title', 'title_pl', 'byline', 'byline_pl', 'text', 'text_pl']}),
        ('Images',  {'fields': ['main_image', 'images']}),
        ('Dates',   {'fields': ['created_date', 'published_date']}),
        ('Links',   {'fields': ['instagram_link', 'twitter_link', 'facebook_link']}),
    ]

    filter_horizontal = ('tag', 'category', 'place', 'images',)


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded', 'taken')

    fieldsets = [
        (None,    {'fields': ['name', 'picture', 'trip']}),
        ('Dates', {'fields': ['taken', 'uploaded']}),
    ]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PlaceStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status',)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status',)
    filter_horizontal = ('images', 'trip',)

    inlines = [
        PostsInLine,
    ]


class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'start_date', 'end_date')

    fieldsets = [
        (None, {'fields': ['name', 'name_pl', 'destination']}),
        ('Dates', {'fields': ['start_date', 'end_date']}),
    ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'bio')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 60})},
    }

    inlines = [
        PostInline,
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_date',)


# Registering

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PlaceStatus, PlaceStatusAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Comment, CommentAdmin)