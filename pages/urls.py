from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/add", views.post_add, name="poast_add"),
    path("post/<int:pk>", views.post_page, name="post_page"),
    path("post/delete/<int:pk>", views.post_delete, name="post_delete"),
    path("post/reaction/<int:pk>", views.add_interaction, name="interaction"),
    path("messages/", views.messages_page, name="messages"),
    path(
        "messages/<str:pk1>/with/<str:pk2>",
        views.send_message_page,
        name="send_message",
    ),
    path("messages/delete/<str:pk>", views.delete_chat, name="delete_chat"),
]
