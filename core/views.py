from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, AthleteProfileForm, MessageForm
from .models import AthleteProfile, Message, User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_athlete:
        profile, _ = AthleteProfile.objects.get_or_create(user=request.user)
        return render(request, 'core/dashboard_athlete.html', {'profile': profile})
    elif request.user.is_club:
        athletes = AthleteProfile.objects.all()
        return render(request, 'core/dashboard_club.html', {'athletes': athletes})
    return redirect('logout')

@login_required
def edit_profile(request):
    profile, _ = AthleteProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AthleteProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AthleteProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def send_message(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('dashboard')
    else:
        form = MessageForm(initial={'receiver': receiver})
    return render(request, 'core/send_message.html', {'form': form, 'receiver': receiver})

def home(request):
    return render(request, 'core/home.html')  # Crie este template
