from django.contrib import admin
from .models import Post, Tag, SharedPost, TaggedPost


class PostAdmin(admin.ModelAdmin):

    exclude = ('slug',)
    list_display = ('id', 'title', 'status', 'author', 'created', 'updated', 'published',)
    list_filter = ('status', 'privacy',)
    search_fields = ('title', 'content',)


class SharedPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user',)


class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'tag',)


# Models registration
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(SharedPost, SharedPostAdmin)
admin.site.register(TaggedPost, TagPostAdmin)
