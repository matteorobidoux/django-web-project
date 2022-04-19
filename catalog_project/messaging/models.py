from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    content = models.TextField(max_length=500)
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reciever')
