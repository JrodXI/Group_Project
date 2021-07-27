from django.urls import path, include
from . import views
from .views import HomePageView, CreateProfileView

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('images', HomePageView.as_view(), name='images.html'),
    path('profile',views.profile),
    path('team_schedule',views.team_schedule),
    path('edit_account',views.edit_account),
    path('<int:user_id>/update_profile',views.update_profile),
    path('<int:team_id>/updatelogo',views.update_logo),
    path('<int:team_id>/join',views.join),
    path('<int:team_id>/remove',views.remove),
    path('logout',views.logout),

]