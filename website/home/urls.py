from django.urls import path, include
from . import views

# URLConf
urlpatterns = [
    path('home/' ,views.get_view)
]