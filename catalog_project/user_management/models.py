from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    # Define the class for permissions
    class Meta:
        permissions = (
            ("add_member", "Add member"),
            ("delete_member", "Add member"),
            ("block_member", "Block member"),
            ("warn_member", "Warn member"),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    flagged = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()


class Warning(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Incase a user gets deleted but you want to log warnings