from django.contrib import admin
from .models import Post, Tag
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.


class PostAdmin(admin.ModelAdmin):

    exclude = ('slug',)
    list_display = ('title', 'status', 'author', 'created', 'updated',)
    list_filter = ('status', 'tags',)
    search_fields = ('title', 'content',)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)