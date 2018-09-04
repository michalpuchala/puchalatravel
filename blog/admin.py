from django.contrib import admin
from blog.models import Category, Tag, Author, Trip, Image, Post

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Trip)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)