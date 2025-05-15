from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, AthleteProfile, Message

admin.site.register(User)
admin.site.register(AthleteProfile)
admin.site.register(Message)
