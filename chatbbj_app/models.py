# models.py
from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    user = models.TextField()
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat_{self.id}"
