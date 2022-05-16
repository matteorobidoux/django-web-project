from django.db import models
from django.contrib.auth.models import User
from item_catalog.models import save_thumbnail_image

# This is the profile attached to the user
# Allows them to be flagged, blocked and get a profile picture
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

    image = models.ImageField(default='profile_pics/default-user.png', upload_to='profile_pics')
    flagged = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    objects = models.Manager()

    # Save resizes the profile picture before actually saving it
    def save(self, *args, **kwargs):
        # Reduce image resolution
        save_thumbnail_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'

    # Gets the latest flag on a profile
    def latest_flag(self):
        flag = self.user.flag_user_target.order_by('-timestamp')[0]
        return flag


# A warning for the user
class Warning(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)

    # In case a user gets deleted, but you want to log warnings
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)