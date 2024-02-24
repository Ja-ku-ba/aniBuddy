from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
  list_display = ("description"[:50], "added")

# Register your models here.
admin.site.register(Post, PostAdmin)