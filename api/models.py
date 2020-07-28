from django.contrib.auth.models import User
from django.db import models


class Pomodoro(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.added} -> {self.notes} ({self.user.username})'

    class Meta:
        ordering = ['-added']
