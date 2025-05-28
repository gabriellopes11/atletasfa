from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('send-message/<int:receiver_id>/', views.send_message, name='send_message'),

    # ✅ Adicionado: rota para exibir perfil de atleta
    path('athlete-profile/<int:user_id>/', views.athlete_profile, name='athlete_profile'),

    # Novas URLs para vídeos e mensagens
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/new/', views.VideoCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('post-video/', views.post_video, name='post_video'),
    path('users/', views.user_list, name='user_list'),
    path('inbox/', views.inbox, name='inbox'),
]
