from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from user_management.models import Profile
from item_catalog.models import Item, Rating, Comment
from messaging.models import Message
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

    # Gets the needed json files stored within the current working directory
    def __get_files(self):
        # Get json perms file
        permissions_path = "permissions.json"

        permissions_json_file = open(permissions_path)
        self.permissions_file = json.load(permissions_json_file)
        permissions_json_file.close()

        # Get post data file
        posts_path = "posts.json"
        posts_json_file = open(posts_path)
        self.posts_file = json.load(posts_json_file)
        posts_json_file.close()

    # Adds superusers to the site
    def __add_superusers(self):
        # add nasr
        superuser = User.objects.create_user('nasr', 'nasr@notanemail.com', '123')
        superuser.groups.add(self.groups['superuser'])
        Profile(user=superuser).save()

    # Adds member admins to the site
    def __add_member_admins(self):
        # add user_manager1
        member_admin1 = User.objects.create_user('user_manager1', 'admin1@notanemail.com', '456')
        member_admin1.groups.add(self.groups['member_admin'])
        Profile(user=member_admin1).save()

        # add user_manager2
        member_admin2 = User.objects.create_user('user_manager2', 'admin3@notanemail.com', '456')
        member_admin2.groups.add(self.groups['member_admin'])
        Profile(user=member_admin2).save()

    # Adds item admins to the site
    def __add_item_admins(self):
        # add item_manager1
        item_admin1 = User.objects.create_user('item_manager1', 'admin2@notanemail.com', '789')
        item_admin1.groups.add(self.groups['item_admin'])
        Profile(user=item_admin1).save()

        # add item_manager2
        item_admin2 = User.objects.create_user('item_manager2', 'admin4@notanemail.com', '789')
        item_admin2.groups.add(self.groups['item_admin'])
        Profile(user=item_admin2).save()

    # Adds 10 members to the site
    def __add_members(self):
        usernames = [
            'John',
            'ResearchGateReposter',
            'John2',
            'Dirk',
            'Lee',
            'Rim',
            'nic',
            'Deeam',
            'Matteo',
            'Oleks'
        ]
        password = 'password'
        for username in usernames:
            member = User.objects.create_user(username, password=password)
            member.groups.add(self.groups['member'])
            Profile(user=member).save()

    # Creates 20 posts using the json posts file
    def __create_content(self):
        stock_comments = [
            'Wow! This is a very interesting research paper.',
            'I am very enthralled by this',
            'This very much is not a repost of an existing paper.',
            'You have too much free time on your hands',
            'I find this study promising',
            "Not sure if I agree with this one...",
            'Amazing.',
            '10/10',
        ]

        for post_data in self.posts_file['posts']:
            post = Item(
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

            # Generate ratings for each post
            for i in range(len(post_data['field'])):
                user_id = i % (User.objects.all().count()-1)+1
                picked_user = User.objects.get(id=user_id)
                # Wrap in a try/catch incase it tries to re-add an existing user
                try:
                    rating = min((len(picked_user.username)) % 5 + (len(post_data['field']) % 5), 5)
                    rate = Rating(rate=rating, item=post, user=picked_user)
                    rate.save()
                except:
                    pass

            # Generate comments for each post
            for i in range(len(post_data['type'])):
                user_id = i % (User.objects.all().count()-1) + 1
                picked_user = User.objects.get(id=user_id)
                # Create a comment for every 2 characters in a post type
                if i % 2 == 0:
                    picked_comment = (i+len(post_data['field'])) % len(stock_comments)
                    comment_message = stock_comments[picked_comment]
                    comment = Comment(content=comment_message, commenter=picked_user, item=post)
                    comment.save()

            # Generate likes for each post, for every keyword they have
            for i in range(len(post_data['keyword_list'].split(','))):
                user_id = i % (User.objects.all().count()-1) + 1
                picked_user = User.objects.get(id=user_id)
                if picked_user not in post.likes.all():
                    post.likes.add(picked_user)

        print("Created content.")

    # Adds the dev user
    def __add_dev(self):
        # add the dev, which can access the django-admin for development purposes
        dev = User.objects.create_superuser("dev", "", "dev")
        dev.groups.add(self.groups['superuser'])
        Profile(user=dev).save()

        print("Added dev user")

    # Create messages sent between users
    def __create_messages(self):
        stock_messages = [
            'Hi, this is my message to you.',
            'I have an even amount of characters in my username.',
            'How are you doing?',
            'Did you get the groceries yet'
        ]
        superuser = User.objects.filter(groups__name='Superuser').first()
        for user in User.objects.all():
            # Create a "greeting message" sent out by the superuser
            if user.id != superuser.id:
                message_content = "Welcome to the site! You are one of our first test users."
                message = Message(sender=superuser, receiver=user, content=message_content)
                message.save()

            # If the user has a username with an even amount of letters, send a message to another user.
            # Or if they have a message sent to them, they can reply if their username has an odd amount of letters
            if (len(user.username) % 2 == 0) or \
                    (len(user.username) % 2 == 1 and Message.objects.filter(receiver=user).exists()):

                message_content = stock_messages[len(user.username) % len(stock_messages)]
                receiver_id = (len(user.username)+10) % (User.objects.all().count()-1)+1
                receiver = User.objects.get(id=receiver_id)
                message = Message(sender=user, receiver=receiver, content=message_content)
                message.save()

    def __create_users(self):
        self.__add_superusers()
        self.__add_item_admins()
        self.__add_member_admins()
        self.__add_members()
        print("Added users")

    # Creates the permissions for all groups
    def __create_permissions(self):
        for group_name in self.permissions_file["groups"].keys():
            for permission_name in self.permissions_file["groups"][group_name]:
                if not Permission.objects.filter(codename=permission_name).exists():
                    print(f"Permission does not exist: {permission_name}")
                    return

    # Creates all 4 groups for the site
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

    # Flushes the database
    def __clear_database(self):
        from django.core.management import call_command
        call_command('flush', interactive=False)
        print("Flushed database.")

    def handle(self, *args, **options):
        # Setup files
        try:
            self.__get_files()
        except FileNotFoundError:
            print("Failed to get json files.")
            print("Make sure posts.json and permissions.json are in your current working directory.")
            print("Quitting...")
            return
        # Flush DB
        self.__clear_database()
        # Create DB
        try:
            self.__create_permissions()
            self.__create_groups()
            self.__create_users()
            self.__create_content()
            self.__create_messages()

            # Create dev on default, don't if --nodev is provided
            if not options.get('nodev'):
                self.__add_dev()

        except BaseException as err: # If something went wrong, flush the database
            print(f"Failed to generate database: {err}")
            self.__clear_database()
            print("Quitting...")