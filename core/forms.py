from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AthleteProfile, Message, VideoPost

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
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Atacante, Zagueiro, Goleiro'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 1.85'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 75'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 23'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre você, sua carreira e objetivos'}),
            'video_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ['title', 'description', 'video_url', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }
