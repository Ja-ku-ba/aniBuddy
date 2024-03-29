from django.contrib import admin

from .models import MyUserModel


# Register your models here.
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ("email"[:45], "username"[:45], "account_created", "deleted")


# Register your models here.
admin.site.register(MyUserModel, MyUserModelAdmin)
