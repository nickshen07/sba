from django.urls import path
from . import views

urlpatterns = [
    path('', views.redir, name="redirect"),
    path('home', views.home, name="home"),
    path('add', views.add, name="add"),
    path('delete', views.delete, name="delete"),
    path('query', views.query, name="query"),
    path('hkoi', views.hkoi, name="hkoi")
]
