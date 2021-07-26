from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from .models import *
import bcrypt
import json
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items(): 
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/home')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/home')

def home(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id = request.session['user_id'])
    context = {
		"user": user,
		"user_teams":Team.objects.filter(captain = user),
        "joined_teams" : Team.objects.filter(joined=user),
		"other_teams": Team.objects.all().exclude(captain=user).exclude(joined=user),
	}
    return render(request,"teams.html",context) 

class HomePageView(ListView):
    model = User, Team
    template_name = 'images.html'