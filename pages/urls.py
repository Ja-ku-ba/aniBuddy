from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/<str:page>", views.add, name="add"),
    path("post/<int:id>", views.post_page, name="post_page"),
    path("post/delete/<int:id>", views.delete_post, name="post_delete"),
]
