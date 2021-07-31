from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.TextField()
    completed = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'