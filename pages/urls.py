from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/add", views.post_add, name="poast_add"),
    path("post/<int:id>", views.post_page, name="post_page"),
    path("post/delete/<int:id>", views.post_delete, name="post_delete"),
]
