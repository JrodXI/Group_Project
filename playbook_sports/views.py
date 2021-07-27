from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import ProfileForm, TeamForm
from .models import *
from django.db.models import Q
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
    userteams = Team.objects.filter(Q(captain = user) | Q(joined = user)).order_by("captain")
    joinedteams = Team.objects.filter(joined = user)
    context = {
		"user": user,
		"user_teams":userteams,
        "joined_teams" : joinedteams,
		"other_teams": Team.objects.all().exclude(captain=user).exclude(joined=user),
	}
    return render(request,"homepage.html",context) 


def profile(request):
    user = User.objects.get(id = request.session['user_id'])

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.update(request.session['user_id'])
            img_obj = form.instance
            logoform = TeamForm
            context={
                'user': user,
                "user_teams":Team.objects.filter(captain = user),
                "form": form,
                "logoform": logoform,
                "img_obj": img_obj
            }
            return render(request,"profile.html",context)
    else:
        form = ProfileForm
        logoform = TeamForm
    
    context={
        'user': user,
        "user_teams":Team.objects.filter(captain = user),
        "form": form,
        "logoform": logoform
        
    }
    return render(request, "profile.html",context)


def update_profile(request, user_id):
    user = User.objects.get(id = user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.update(request.session['user_id'])
            img_obj = form.instance
            
        return redirect("/profile")


def team_schedule(request):
    return render(request, "team_schedule.html")

def edit_account(request):
    return render(request, "update_profile.html")

def update_logo(request,team_id):
    user = User.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        logoform = TeamForm(request.POST, request.FILES)
        if logoform.is_valid():
            logoform.update(team_id)
        return redirect("/profile")

def join(request, team_id):
    user = User.objects.get(id = request.session['user_id'])
    joined_team = Team.objects.get(id= team_id)
    joined_team.joined.add(user)
    joined_team.save()
    return redirect ('/home')

def remove(request, team_id):
    user = User.objects.get(id = request.session['user_id'])
    joined_team = Team.objects.get(id= team_id)
    joined_team.joined.remove(user)
    joined_team.save()
    return redirect ('/home')






def logout(request):
    request.session.flush()
    return redirect('/')

class HomePageView(ListView):
    model = User, Team
    template_name = 'images.html'

class CreateProfileView(CreateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'


class CreateTeamView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'profile.html'
