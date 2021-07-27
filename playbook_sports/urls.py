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
    path('edit_team', views.edit_team),
    path('<int:user_id>/update_profile',views.update_profile), #this is for updating the image on the profile page
    path('<int:team_id>/updatelogo',views.update_logo), #this is to update logo on profile page
    path('<int:team_id>/join',views.join), #this is for homepage table 
    path('<int:team_id>/remove',views.remove), #this is for homepage table
    path('logout',views.logout),

]

#for anyone needing to add backend data feel free to change what you need.
# I only set up paths for the sake of navigating while doing frontend.