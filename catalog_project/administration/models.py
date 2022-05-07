from django.db import models
from django.contrib.auth.models import User, Group
# Create a list of all permissions for the admin group

class SitePermissions(models.Model):
    class Meta:
        permissions = (
            ("block_user", "Block User"),
            ("flag_user", "Flag User"),
            ("view_dashboard", "View dashboard")
        )


class UserFlag(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='user_target')
    timestamp = models.DateTimeField(auto_now_add=True)
    blame = models.ForeignKey(User, models.CASCADE, related_name='user_blame')