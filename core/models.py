from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Usuário customizado
class User(AbstractUser):
    is_athlete = models.BooleanField(default=False)
    is_club = models.BooleanField(default=False)

# Perfil de atleta
class AthleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    height = models.FloatField(help_text="Em metros")
    weight = models.FloatField(help_text="Em kg")
    age = models.PositiveIntegerField()
    bio = models.TextField()
    video_link = models.URLField(blank=True)
    photo = models.ImageField(upload_to='athletes/', blank=True)

    def __str__(self):
        return self.full_name

# Mensagens entre clubes e atletas
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.sender} para {self.receiver}"
