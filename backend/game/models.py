from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GameSession(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    dm = models.ForeignKey(User, related_name='dmsessions', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(GameSession, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hp = models.IntegerField(default=10)
    attack = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class NPC(models.Model):
    game = models.ForeignKey(GameSession, related_name='npcs', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hp = models.IntegerField(default=5)
    attack = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Message(models.Model):
    game = models.ForeignKey(GameSession, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    is_dm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'DM' if self.is_dm else self.author}: {self.content[:30]}"
