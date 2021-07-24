from django.urls import path
from . import views
from .views import HomePageView

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('images', HomePageView.as_view(), name='images'),
]