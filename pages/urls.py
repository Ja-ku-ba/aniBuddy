from . import views

from django.urls import path

urlpatterns = [
    path("", views.home, name='home'),
    path("add/<str:page>", views.add, name='add')
]
