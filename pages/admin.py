from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
  list_display = ("description_char"[:50], "added")

# Register your models here.
admin.site.register(Post, PostAdmin)