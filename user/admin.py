from django.contrib import admin

from .models import MyUserModel


# Register your models here.
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ("email"[:35], "username"[:35], "account_created", "deleted")


# Register your models here.
admin.site.register(MyUserModel, MyUserModelAdmin)
