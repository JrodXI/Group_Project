from django.urls import path
from . import views
from .views import HomePageView, CreateProfileView

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('images', HomePageView.as_view(), name='images.html'),
    path('<int:user_id>/profile',views.profile),
    path('logout',views.logout),
    path('user/',CreateProfileView.as_view(), name='images')


]