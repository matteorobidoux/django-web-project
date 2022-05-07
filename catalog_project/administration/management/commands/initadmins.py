from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from user_management.models import Profile
from item_catalog.models import Item
import json

class Command(BaseCommand):
    help = "Initializes the website with all the admin users"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--nodev',
            action='store_true',
            help='Does not create the dev user',
        )

    def __get_files(self):
        # Get json perms file
        permissions_path = "permissions.json"

        permissions_json_file = open(permissions_path, encoding='utf8')
        self.permissions_file = json.load(permissions_json_file)
        permissions_json_file.close()

        # Get post data file
        posts_path = "posts.json"
        posts_json_file = open(posts_path, encoding='utf8')
        self.posts_file = json.load(posts_json_file)
        posts_json_file.close()

    def __add_superusers(self):
        # add nasr
        superuser = User.objects.create_user('nasr', 'nasr@notanemail.com', '123')
        superuser.groups.add(self.groups['superuser'])
        Profile(user=superuser).save()

    def __add_member_admins(self):
        # add user_manager1
        member_admin1 = User.objects.create_user('user_manager1', 'admin1@notanemail.com', '456')
        member_admin1.groups.add(self.groups['member_admin'])
        Profile(user=member_admin1).save()

        # add user_manager2
        member_admin2 = User.objects.create_user('user_manager2', 'admin3@notanemail.com', '456')
        member_admin2.groups.add(self.groups['member_admin'])
        Profile(user=member_admin2).save()

    def __add_item_admins(self):
        # add item_manager1
        item_admin1 = User.objects.create_user('item_manager1', 'admin2@notanemail.com', '789')
        item_admin1.groups.add(self.groups['item_admin'])
        Profile(user=item_admin1).save()

        # add item_manager2
        item_admin2 = User.objects.create_user('item_manager2', 'admin4@notanemail.com', '789')
        item_admin2.groups.add(self.groups['item_admin'])
        Profile(user=item_admin2).save()

    def __add_members(self):
        usernames = [
            'John',
            'ResearchGateReposter',
            'John2',
            'Dirk',
            'Lee',
            'Rim',
            'Nicoleta',
            'Deeam',
            'Matteo',
            'Oleks'
        ]
        password = 'password'
        for username in usernames:
            member = User.objects.create_user(username, password=password)
            member.groups.add(self.groups['member'])
            Profile(user=member).save()

    def __create_content(self):
        for post_data in self.posts_file['posts']:
            post = Item(
                id=post_data['id'],
                name=post_data['name'],
                owner=User.objects.get(id=post_data['owner']),
                type=post_data['type'],
                field=post_data['field'],
                keyword_list=post_data['keyword_list'],
                content=post_data['content'],
                url=post_data['url'],
                status=post_data['status']
            )
            post.save()
        print("Created content.")

    def __add_dev(self):
        # add the dev, which can access the django-admin for development purposes
        dev = User.objects.create_superuser("dev", "", "dev")
        dev.groups.add(self.groups['superuser'])
        Profile(user=dev).save()

        print("Added dev user")

    def __create_users(self):
        self.__add_superusers()
        self.__add_item_admins()
        self.__add_member_admins()
        self.__add_members()
        print("Added users")

    def __create_permissions(self):
        for group_name in self.permissions_file["groups"].keys():
            for permission_name in self.permissions_file["groups"][group_name]:
                if not Permission.objects.filter(codename=permission_name).exists():
                    print(f"Permission does not exist: {permission_name}")
                    return

    def __create_groups(self):
        # Create groups
        superuser_group = Group.objects.create(name="Superuser")
        member_admin_group = Group.objects.create(name="MemberAdmin")
        item_admin_group = Group.objects.create(name="ItemAdmin")
        member_group = Group.objects.create(name="Member")
        groups = {
            'superuser': superuser_group,
            'member_admin': member_admin_group,
            'item_admin': item_admin_group,
            'member': member_group
        }
        self.groups = groups
        print("Created groups.")

        # Add permissions to groups
        for group_name in self.permissions_file["groups"].keys():
            group = Group.objects.get(name=group_name)
            for permission_name in self.permissions_file["groups"][group_name]:
                permission = Permission.objects.get(codename=permission_name)
                group.permissions.add(permission)
        print("Added permissions to groups.")

    def __clear_users(self):
        from django.core.management import call_command
        call_command('flush')
        print("Flushed database.")

    def handle(self, *args, **options):
        try:
            self.__get_files()
        except FileNotFoundError:
            print("Failed to get json files.")
            print("Make sure posts.json and permissions.json are in your current working directory.")
            print("Quitting...")
            return

        self.__clear_users()
        self.__create_permissions()
        self.__create_groups()
        self.__create_users()
        self.__create_content()

        if not options.get('nodev'):
            self.__add_dev()
