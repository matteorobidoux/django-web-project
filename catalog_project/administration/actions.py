from django.contrib.auth.models import User
from user_management.models import Warning, Profile

def get_user(id):
    return User.objects.get(id=id)

def warn_user(request, id):
    message = request.POST.get('warning-message')
    warning = Warning(message=message, user=get_user(id))
    warning.save()

def flag_user(request, id):
    profile = Profile.objects.get(user=get_user(id))
    profile.flagged = not profile.flagged
    profile.save()

def block_user(request, id):
    profile = Profile.objects.get(user=get_user(id))
    profile.blocked = not profile.blocked
    profile.save()

def edit_user(request, id):
    pass

def delete_user(request, id):
    get_user(id).delete()
