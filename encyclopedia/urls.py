from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.render_page, name="render_page"),
    path("search/", views.search_page, name="search_page"),
    path("newpage/", views.new_page, name="new_page"),
    path("wiki/<str:title>/edit_page/", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page")
]
