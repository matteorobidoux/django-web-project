from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse

CUTOFF_LENGTH = 50

# Create your models here.

# Represents messages sent between users
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    content = models.TextField(max_length=500, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('inbox')

    def __str__(self):
        # Show ellipses if text is cut off
        text = self.content[:CUTOFF_LENGTH]
        return text if len(self.content) <= CUTOFF_LENGTH else text+"..."
