from django.urls import path
from .views import home, search


urlpatterns = [
    path('home', view=home, name="home"),
    path('search/', view=search, name="search"),
]
