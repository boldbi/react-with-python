from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_embed_details', views.get_embed_details, name = "get_embed_details"),
]