from django.db import models
from django.contrib.auth.models import User

CUTOFF_LENGTH = 50

# Create your models here.
class Message(models.Model):
    content = models.TextField(max_length=500)
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reciever')

    def __str__(self):
        text = self.content[:CUTOFF_LENGTH]
        return text if len(self.content) <= CUTOFF_LENGTH else text+"..."
