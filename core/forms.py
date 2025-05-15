from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AthleteProfile, Message

class UserRegisterForm(UserCreationForm):
    is_athlete = forms.BooleanField(required=False)
    is_club = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_athlete', 'is_club']

class AthleteProfileForm(forms.ModelForm):
    class Meta:
        model = AthleteProfile
        fields = ['full_name', 'position', 'height', 'weight', 'age', 'bio', 'video_link', 'photo']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
