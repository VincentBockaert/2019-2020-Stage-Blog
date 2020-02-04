from django.contrib import admin

# Register your models here.

from .models import Author, Blog

class BlogInline(admin.StackedInline):
    model = Blog
    extra = 2


class BlogAdmin(admin.ModelAdmin):
    fields = ['title','author','pub_date','description','content']

class AuthorAdmin(admin.ModelAdmin):
    fields = ['full_name']
    inlines = [BlogInline]

admin.site.register(Author)
admin.site.register(Blog, BlogAdmin)


