from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuário customizado
class User(AbstractUser):
    is_athlete = models.BooleanField(default=False)
    is_club = models.BooleanField(default=False)

# Perfil de atleta
class AthleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, default='')
    position = models.CharField(max_length=50, blank=True, default='')
    height = models.FloatField(help_text="Em metros", null=True, blank=True, default=None)
    weight = models.FloatField(help_text="Em kg", null=True, blank=True, default=None)
    age = models.PositiveIntegerField(null=True, blank=True, default=None)
    bio = models.TextField(blank=True, default='')
    video_link = models.URLField(blank=True, default='')
    photo = models.ImageField(upload_to='athletes/', blank=True)

    def __str__(self):
        return self.full_name or self.user.username

# Perfil de clube
class ClubProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='club_profile')
    name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)
    
    def __str__(self):
        return self.name or self.user.username

# Mensagens entre clubes e atletas
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.sender} para {self.receiver}"

class VideoPost(models.Model):
    user = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text="URL do YouTube ou Vimeo")
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
