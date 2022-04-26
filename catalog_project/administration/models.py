from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
#TODO:
# Add all four groups: Member, Superuser admin, Item admin and User admin
# Hierarchy:
# Superuser admin
# Item admin/user admin
# Member
# Permissions for all four groups:

# Create a list of all permissions for the admin group

class SitePermissions(models.Model):
    class Meta:
        permissions = (
            ("block_user", "Block User"),
            ("flag_user", "Flag User"),
        )