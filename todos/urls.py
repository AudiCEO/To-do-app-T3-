from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("toggle/<int:pk>/", views.toggle, name="toggle"),
    path("delete/<int:pk>/", views.delete, name="delete"),
]
