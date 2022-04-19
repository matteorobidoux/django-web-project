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
            ("Add Item", "add_item"),
            ("Delete Item", "delete_item"),
            ("Edit Item", "edit_item"),
            ("Rate Item", "rate_item"),
            ("Comment", "comment"),
            ("Message Users", "chat"),

            ("Add Member", "add_member"),
            ("Delete Member", "delete_member"),
            ("Block Member", "block_member"),
            ("Warn Member", "warn_member"),

            ("Add Any Item", "add_any_item"),
            ("Remove Any Item", "remove_any_item"),
            ("Edit Any Item", "edit_any_item"),

            ("Add User", "add_user"),
            ("Delete User", "delete_user"),
            ("Block User", "block_user"),
            ("Warn User", "warn_user"),
            ("Flag User", "flag_user"),
            ("Change User Group", "chgrp_user")
        )
