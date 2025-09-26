from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_dm_chat, name='ai_dm_chat'),
]