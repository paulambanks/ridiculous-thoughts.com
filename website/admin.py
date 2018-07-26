from django.contrib import admin
from .models import Post, Tag, SharedPost, TagPost


class PostAdmin(admin.ModelAdmin):

    exclude = ('slug',)
    list_display = ('id', 'title', 'status', 'author', 'created', 'updated', 'published',)
    list_filter = ('status', 'privacy',)
    search_fields = ('title', 'content',)


class SharedPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'shared_post', 'shared_with',)


class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tagged_post', 'tagged_with',)


# Models registration
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(SharedPost, SharedPostAdmin)
admin.site.register(TagPost, TagPostAdmin)
