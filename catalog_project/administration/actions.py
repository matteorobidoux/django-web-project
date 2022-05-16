from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from notifications.signals import notify
from user_management.models import Warning, Profile
from item_catalog.models import Item, ItemFlag
from .models import UserFlag
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION


# Gets a user by id
def get_user(id):
    return User.objects.get(id=id)


# Action for warning the user
def warn_user(request, id):
    # Create a warning entry
    message = request.POST.get('warning-message')
    warning = Warning(message=message, user=get_user(id))
    warning.save()

    # Log action
    log_message = f'Warned {warning.user.username} with "{warning.message}"'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Warning).pk,
        object_id=warning.id,
        object_repr=log_message,
        action_flag=ADDITION
    )
    notify.send(request.user, recipient=warning.user, verb='Warning', description=warning.message)
    log.save()


# Action for flagging the user
def flag_user(request, id):
    # Set flag on profile
    user = get_user(id)
    profile = user.profile
    profile.flagged = not profile.flagged
    if profile.flagged:
        UserFlag(user=user, blame=request.user).save()

    profile.save()

    # Log action
    action_name = "Flagged" if profile.flagged else "Unflagged"
    log_message = f'{action_name} {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Profile).pk,
        object_id=profile.id,
        object_repr=log_message,
        action_flag=CHANGE
    )
    log.save()


# Action for blocking the user
def block_user(request, id):
    # Set block flag on user
    user = get_user(id)
    profile = Profile.objects.get(user=user)
    profile.blocked = not profile.blocked
    profile.save()

    # Log action
    action_name = "Blocked" if profile.blocked else "Unblocked"
    log_message = f'{action_name} {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Profile).pk,
        object_id=profile.id,
        object_repr=log_message,
        action_flag=CHANGE
    )
    log.save()


# Action for editing the user
def edit_user(request, id):
    user = get_user(id)
    # Log action
    log_message = f'Edited {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(User).pk,
        object_id=user.id,
        object_repr=log_message,
        action_flag=CHANGE
    )
    log.save()


# Action for creating the user
def create_user(request, id):
    user = get_user(id)
    # Log action
    log_message = f'Created {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(User).pk,
        object_id=user.id,
        object_repr=log_message,
        action_flag=ADDITION
    )
    log.save()


# Action for deleting the user
def delete_user(request, id):
    user = get_user(id)
    # Log action
    log_message = f'Deleted {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(User).pk,
        object_id=user.id,
        object_repr=log_message,
        action_flag=DELETION
    )
    log.save()


# Action for editing an item
def edit_item(request, id):
    item = Item.objects.get(id=id)
    # Log action
    log_message = f'Edited {item.name}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Item).pk,
        object_id=item.id,
        object_repr=log_message,
        action_flag=CHANGE
    )
    log.save()


# Action for deleting an item
def delete_item(request, id):
    item = Item.objects.get(id=id)
    # Log action
    log_message = f'Deleted {item.name}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Item).pk,
        object_id=item.id,
        object_repr=log_message,
        action_flag=DELETION
    )
    log.save()


# Action for flagging an item
def flag_item(request, id):
    # Set flag for item
    item = Item.objects.get(id=id)
    item.flagged = not item.flagged
    if item.flagged:
        ItemFlag(item=item, blame=request.user).save()
    item.save()

    # Log action
    action_name = "Flagged" if item.flagged else "Unflagged"
    log_message = f'{action_name} {item.name}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Item).pk,
        object_id=item.id,
        object_repr=log_message,
        action_flag=CHANGE
    )
    log.save()

