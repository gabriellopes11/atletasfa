from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
# Adicionar a importação da função login
from django.contrib.auth import login

# Importação dos modelos
from .models import AthleteProfile, Message, User, VideoPost
from .forms import UserRegisterForm, AthleteProfileForm, MessageForm, VideoPostForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Agora a função login está disponível
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_athlete:
        # Usando get_or_create com defaults vazios para evitar erros de NULL
        profile, created = AthleteProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': '',
                'position': '',
                'height': None,
                'weight': None,
                'age': None,
                'bio': '',
                'video_link': ''
            }
        )
        return render(request, 'core/dashboard_athlete.html', {'profile': profile})
    elif request.user.is_club:
        athletes = AthleteProfile.objects.all()
        return render(request, 'core/dashboard_club.html', {'athletes': athletes})
    return redirect('logout')

@login_required
def edit_profile(request):
    profile, created = AthleteProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AthleteProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao atualizar perfil. Por favor, verifique os campos.')
    else:
        form = AthleteProfileForm(instance=profile)
    
    return render(request, 'core/edit_profile.html', {'form': form, 'profile': profile})

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

class VideoListView(ListView):
    model = VideoPost
    template_name = 'core/video_list.html'
    context_object_name = 'videos'
    ordering = ['-created_at']
    paginate_by = 12

class VideoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = VideoPost
    form_class = VideoPostForm
    template_name = 'core/video_create.html'
    success_url = reverse_lazy('video_list')
    success_message = "Seu vídeo foi postado com sucesso!"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class VideoDetailView(DetailView):
    model = VideoPost
    template_name = 'core/video_detail.html'
    context_object_name = 'video'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar formulário de mensagem ao contexto
        context['message_form'] = MessageForm()
        return context

@login_required
def user_list(request):
    """Lista de usuários para enviar mensagens"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'core/user_list.html', {'users': users})

@login_required
def inbox(request):
    """Caixa de entrada de mensagens do usuário"""
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'core/inbox.html', {'messages': messages})

@login_required
def post_video(request):
    if request.method == 'POST':
        form = VideoPostForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, 'Vídeo postado com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao postar vídeo. Por favor, verifique os campos.')
    else:
        form = VideoPostForm()
    return render(request, 'core/post_video.html', {'form': form})
