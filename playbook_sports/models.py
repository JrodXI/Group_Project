from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        #validate first name
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"
        #validate last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"
        #email matches format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['email'])==0:
            errors['email'] = "You must enter an email"
            
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"
        #email is unique
        current_users = User.objects.filter(email = postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"
        #password was enteres (less than 8) and reconfirm password matches
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
            
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        #email has been entered
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        #password has been entered
        if len(postData['password']) == 0:
            errors['password'] = "Password must be entered"
        #if the email and password match
        if not existing_user:
            errors['user'] = "User doesn't exist"
            
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match"
        return errors
        
    def update_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        if len(postData['updated_password']) == 0:
            errors['updated_password'] = "Password must be entered"
        return errors

class TeamManager(models.Manager):
    def team_validator(self, postData):
        errors = {}
        if len(postData['team_name']) < 3:
            errors['team_name'] = "Team Name must at least 3 characters long"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='images/',default='images/profile.png')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.first_name

class Team(models.Model):
    team_name = models.CharField(max_length=255)
    team_sport = models.CharField(max_length=255)
    captain = models.ForeignKey(User, related_name = "teams",on_delete=models.CASCADE)
    joined = models.ManyToManyField(User, related_name = "joined_teams")
    team_logo = models.ImageField(upload_to='images/',default='images/soccer.jpg',null=True)
    objects = TeamManager()

    def __str__(self):
        return self.team_name

class Sport(models.Model):
    sport = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name = 'sports', on_delete=models.CASCADE)