from django.contrib import admin

from .models import Post, PostImage, Reaction, Coment, UserMessage, ChatRoom


class PostAdmin(admin.ModelAdmin):
    list_display = ("description"[:50], "owner"[:50], "added")


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
admin.site.register(Reaction)
admin.site.register(Coment)
admin.site.register(UserMessage)
admin.site.register(ChatRoom)
