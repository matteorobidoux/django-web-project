from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from user_management.models import Warning, Profile
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION


def get_user(id):
    return User.objects.get(id=id)


def warn_user(request, id):
    message = request.POST.get('warning-message')
    warning = Warning(message=message, user=get_user(id))

    warning.save()

    log_message = f'Warned {warning.user.username} with "{warning.message}"'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(Warning).pk,
        object_id=warning.id,
        object_repr=log_message,
        action_flag=ADDITION
    )
    log.save()


def flag_user(request, id):
    user = get_user(id)
    profile = user.profile
    profile.flagged = not profile.flagged
    profile.save()

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


def block_user(request, id):
    user = get_user(id)
    profile = Profile.objects.get(user=user)
    profile.blocked = not profile.blocked
    profile.save()

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


def edit_user(request, id):
    user = get_user(id)
    log_message = f'Edited {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(User).pk,
        object_id=user.id,
        object_repr=log_message,
        action_flag=CHANGE
    )
    log.save()


def delete_user(request, id):
    user = get_user(id)
    log_message = f'Deleted {user.username}'
    log = LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(User).pk,
        object_id=user.id,
        object_repr=log_message,
        action_flag=DELETION
    )
    log.save()