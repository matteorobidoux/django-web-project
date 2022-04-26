from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from user_management.models import Profile
import json

class Command(BaseCommand):
    help = "Initializes the website with all the admin users"

    def handle(self, *args, **options):
        # Get json perms file
        path_to_file = "permissions.json"
        file = None
        try:
            json_file = open(path_to_file)
            file = json.load(json_file)
        except FileNotFoundError:
            print("Could not get permissions.json. Quitting...")
            return

        for group_name in file["groups"].keys():
            for permission_name in file["groups"][group_name]:
                if Permission.objects.get(codename=permission_name) is None:
                    print(f"Permission does not exist: {permission_name}")

        # Clear groups and users
        Group.objects.all().delete()
        User.objects.all().delete()
        print("Cleared groups and users.")

        # Create groups
        superuser_group = Group.objects.create(name="Superuser")
        member_admin_group = Group.objects.create(name="MemberAdmin")
        item_admin_group = Group.objects.create(name="ItemAdmin")
        member_group = Group.objects.create(name="Member")
        print("Created groups.")

        # Add permissions to groups
        for group_name in file["groups"].keys():
            group = Group.objects.get(name=group_name)
            for permission_name in file["groups"][group_name]:
                permission = Permission.objects.get(codename=permission_name)
                group.permissions.add(permission)
        print("Added permissions to groups.")

        # add nasr
        superuser = User.objects.create_user('nasr', 'nasr@notanemail.com', '123', id=1)
        superuser.groups.add(superuser_group)
        Profile(user=superuser).save()

        # add user_manager1
        member_admin = User.objects.create_user('user_manager1', 'admin1@notanemail.com', '456', id=2)
        member_admin.groups.add(member_admin_group)
        Profile(user=member_admin).save()

        # add item_manager1
        item_admin = User.objects.create_user('item_manager1', 'admin2@notanemail.com', '789', id=3)
        item_admin.groups.add(item_admin_group)
        Profile(user=item_admin).save()

        print("Added users")
        # add the dev, which can access the django-admin for development purposes
        dev = User.objects.create_superuser("dev", "", "dev", id=4)
        dev.groups.add(superuser_group)
        Profile(user=dev).save()

        print("Added dev user")