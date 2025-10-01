from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('lobby/', views.lobby, name='lobby'),
    path('create/', views.create_session, name='create'),
    path('session/<int:session_id>/', views.session_view, name='session'),
    path('session/<int:session_id>/post/', views.post_message, name='post_message'),
]