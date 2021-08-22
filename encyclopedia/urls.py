from unicodedata import name
from django.urls import path

from . import views

app_name = "pea"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="getPage"),
    path("search", views.search, name='search'),
    path("newEntry", views.new_entry, name="new"),
    path("wiki/<str:entryEdit>/edit", views.edit, name="edit"),
    path("random", views.randomPage, name="random")
]
