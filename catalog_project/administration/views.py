from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic, View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import actions
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages


# Main dashboard interface when you open the dashboard. Uses the page as an argument to filter users.
class Dashboard(PermissionRequiredMixin, generic.ListView):
    permission_required = "view_dashboard"
    # Default model is user.
    model = User
    context_object_name = 'user_list'
    template_name = 'dashboard.html'
    paginate_by = 3


""" Dashboard functions """


# The user warning view
class WarnUser(PermissionRequiredMixin, View):
    permission_required = "warn_user"

    # Post executes the warning onto the user
    def post(self, request, *args, **kwargs):
        actions.warn_user(request, kwargs["id"])
        return redirect('/admin')

    # Get shows the warning form page
    def get(self, request, *args, **kwargs):
        user = actions.get_user(kwargs["id"])
        template = loader.get_template('warn-user.html')
        context = {
            'target_user': user
        }
        return HttpResponse(template.render(context, request))


class FlagUser(PermissionRequiredMixin, View):
    permission_required = 'flag_user'

    def post(self, request, *args, **kwargs):
        actions.flag_user(request, kwargs['id'])
        return redirect('/admin')


class BlockUser(PermissionRequiredMixin, View):
    permission_required = "flag_user"

    def post(self, request, *args, **kwargs):
        actions.block_user(request, kwargs['id'])
        return redirect('/admin')


class DeleteUser(PermissionRequiredMixin, View):
    permission_required = "delete_user"

    # Post executes the deletion
    def post(self, request, *args, **kwargs):
        actions.delete_user(request, kwargs['id'])
        return redirect('/admin')

    # Get shows the deletion confirmation page
    def get(self, request, *args, **kwargs):
        template = loader.get_template('delete-user.html')
        context = {
            'target_user': actions.get_user(kwargs['id'])
        }
        return HttpResponse(template.render(context, request))


class EditUserView(PermissionRequiredMixin, View):
    permission_required = "change_user"

    # Post saves the edits on the user and profile
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile has been updated")
            return redirect('/admin')

    # Get shows the edit page
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        initial_user = {
            "email": user.email,
            "password": ""
        }
        initial_profile = {
            "image": user.profile.image,
            "flagged": user.profile.flagged,
            "blocked": user.profile.blocked
        }

        user_form = UserUpdateForm(instance=user, initial=initial_user)
        profile_form = ProfileUpdateForm(instance=user.profile, initial=initial_profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'target_user': user
        }
        template = loader.get_template('edit-user.html')
        return HttpResponse(template.render(context, request))