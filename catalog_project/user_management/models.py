from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # Define the class for permissions
    class Meta:
        permissions = (
            ("add_member", "Add member"),
            ("delete_member", "Delete member"),
            ("block_member", "Block member"),
            ("warn_member", "Warn member"),
            ("flag_member", "Flag member"),
            ("view_member_dashboard", "View member dashboard")
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(default='default-user.png', upload_to='profile_pics')
    flagged = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    objects = models.Manager()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Reduce image resolution when adding in snapshot
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'

    def latest_flag(self):
        flag = self.user.flag_user_target.order_by('-timestamp')[0]
        return flag


class Warning(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Incase a user gets deleted but you want to log warnings