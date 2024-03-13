from django.contrib import admin

from .models import Post, PostImage


class PostAdmin(admin.ModelAdmin):
    list_display = ("description"[:50], "owner"[:50], "added")


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
