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


class Flag(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)