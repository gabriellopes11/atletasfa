from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Importação dos modelos
from .models import AthleteProfile, ClubProfile, Message, User, VideoPost
from .forms import UserRegisterForm, AthleteProfileForm, MessageForm, VideoPostForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário após o registro
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_athlete:
        # Pega ou cria o perfil de atleta para o usuário logado
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
        # Renderiza dashboard simplificado para clubes (a ajustar conforme necessidade)
        return render(request, 'core/dashboard_club.html', {
            'profile': {'name': request.user.username},
            'athletes': [],
            'recent_messages': []
        })
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
    receiver = get_object_or_404(User, id=receiver_id)
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
        # Adiciona formulário para envio de mensagem no detalhe do vídeo
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

@login_required
def athlete_profile(request, user_id):
    """
    Visualização do perfil do atleta.
    - Busca o usuário pelo ID.
    - Se não existir perfil de atleta, mostra mensagem de erro.
    - Caso contrário, mostra os dados do atleta.
    """
    user = get_object_or_404(User, id=user_id)

    # Verifica se o usuário possui perfil de atleta
    if not hasattr(user, 'athleteprofile'):
        return render(request, 'core/athlete_profile_not_found.html', {'user': user})

    # Adicionar logging para verificar o upload
    print(f"Arquivo recebido: {request.FILES.get('photo')}")
    return render(request, 'core/athlete_profile.html', {
        'athlete': user,
        'profile': user.athleteprofile,
    })
