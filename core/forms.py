from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AthleteProfile, Message, VideoPost

# Lista de times para o campo dropdown de seleção
TEAM_CHOICES = [
    ('', 'Selecione o time'),
    ('Rondonopolis Hawks', 'Hawks'),
    ('Cuiabá Arsenal', 'Arsenal'),
    ('Sinop Coyotes', 'Coyotes'),
    ('Galo', 'Galo'),
    ('Remo', 'Remo'),
    # Adicione mais times conforme necessário
]

# Formulário de registro customizado para o usuário
class UserRegisterForm(UserCreationForm):
    is_athlete = forms.BooleanField(required=False)
    is_club = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_athlete', 'is_club']


# Formulário para editar o perfil do atleta
class AthleteProfileForm(forms.ModelForm):
    # Campo de seleção do time (dropdown)
    team = forms.ChoiceField(
        choices=TEAM_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = AthleteProfile
        fields = [
            'full_name', 'position', 'height', 'weight', 'age', 'bio',
            'video_link', 'photo', 'desired_salary', 'needs_housing',
            'needs_food', 'needs_transport', 'team'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Atacante, Zagueiro, Goleiro'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 1.85'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 75'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 23'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conte um pouco sobre você'}),
            'video_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'desired_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salário desejado em USD'}),
            'needs_housing': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'needs_food': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'needs_transport': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    # Validação extra para o campo photo (formato + tamanho)
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            extension = photo.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('Formato de imagem não suportado. Use JPG, PNG, GIF ou WebP.')

            # Limite de tamanho: 5MB (opcional, mas recomendável)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('A imagem deve ter no máximo 5MB.')
        return photo


# Formulário para envio de mensagens entre usuários
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


# Formulário para postagens de vídeo
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
