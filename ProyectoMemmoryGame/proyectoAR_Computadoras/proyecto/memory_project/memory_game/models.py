from django.db import models
from django.contrib.auth.models import User


class GameRecord(models.Model):
    LEVEL_CHOICES = [
        ("basico", "Básico"),
        ("medio", "Medio"),
        ("avanzado", "Avanzado"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_records")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    win = models.BooleanField(default=False)
    duration_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_level_display()} - {'Win' if self.win else 'Loss'}"
