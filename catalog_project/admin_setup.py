import json
from django.contrib.auth.models import User, Group, Permission
# run the shell in manage.py and IMPORT this script
path_to_file = "permissions.json"
file = json.load(open(path_to_file))

def print_meta():
    print("permissions = (")
    for perm in file["permissions"]:
        codename = perm["codename"]
        name = perm["name"]
        print(f"(\"{codename}\",\"{name}\")")
    print(")")

def init_groups_and_users():
    Group.objects.all().delete()
    User.objects.all().delete()
    superuser_group = Group.objects.create(name="Superuser")
    member_admin_group = Group.objects.create(name="MemberAdmin")
    item_admin_group = Group.objects.create(name="ItemAdmin")
    member_group = Group.objects.create(name="Member")
    print("Created groups.")

    #add perms
    for group_name in file["groups"].keys():
        group = Group.objects.get(name=group_name)
        for permission_name in file["groups"][group_name]:
            permission = Permission.objects.get(name=permission_name)
            group.permissions.add(permission)
    print("Added permissions to groups.")

    # add nasr
    superuser = User.objects.create_user('nasr', 'nasr@notanemail.com', '123')
    superuser_group.user_set.add(superuser)
    # add user_manager1
    member_admin = User.objects.create_user('user_manager1', 'admin1@notanemail.com', '456')
    member_admin_group.user_set.add(member_admin)
    # add item_manager1
    item_admin = User.objects.create_user('item_manager1', 'admin2@notanemail.com', '789')
    item_admin_group.user_set.add(item_admin)
    print("Added users")
    # add the dev, which can access the django-admin for development purposes
    dev = User.objects.create_superuser("dev","","dev")
    print("Added dev user")

