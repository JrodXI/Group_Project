from django import forms
from django.forms import widgets
from .models import User, Team


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('profile_pic',)

    def update(self, id_num):
        data = self.cleaned_data
        user = User.objects.get(id=id_num)
        user.profile_pic = data['profile_pic']
        user.save()


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('team_logo',)

    def update(self, id_num):
        data = self.cleaned_data
        team = Team.objects.get(id=id_num)
        team.team_logo = data['team_logo']
        team.save()