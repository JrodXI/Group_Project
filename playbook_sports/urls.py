from django.urls import path, include
from . import views
from .views import HomePageView, newteam

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    # path('images', HomePageView.as_view(), name='images'),
    path('create_team', views.createteam),
    path('new_team', views.newteam),
    path('team_rankings', views.teamrankings)
]