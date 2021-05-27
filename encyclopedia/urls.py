from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create_new", views.create_new, name="create"),
    path("wiki/<str:title>", views.entry, name="entry")
]
