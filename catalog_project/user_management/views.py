from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.views import generic
from django.views.generic import DetailView, DeleteView
from notifications.models import Notification

from .models import Profile
from .user_form import NewUserForm, NewMemberForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import Group
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from administration.views import EditUserView

from administration import actions
from administration.views import ActionView, PostLastPage, UserCreateView, ModelSearchListView, TargetUserView


# Uses has_permission mixin function to check if the action is being enacted on a member
class CheckMemberMixin(PermissionRequiredMixin, TargetUserView):
    def has_permission(self):
        if not self.target.groups.filter(name='Member').exists() or self.target.groups.all().count()>1 :
            return False

        return super().has_permission()


class ManageUsers(PermissionRequiredMixin, ModelSearchListView):
    search_redirect = '/useradmin'
    sort_fields = ('id', 'username', 'email')
    permission_required = 'user_management.view_member_dashboard'
    # Default model is user.
    model = User
    context_object_name = 'users'
    template_name = 'manage-users.html'
    ordering = ['id']
    paginate_by = 10


def profile_page(request, username=None):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view profiles')
        return redirect('/login')
    template = loader.get_template('profile.html')
    if username:
        user_page = get_object_or_404(User, username=username)
        profile = user_page.profile
    else:
        user_page = request.user.username
        profile = request.user.profile
    return HttpResponse(template.render({'profile': profile, 'user': user_page}, request))


def register(request):
    template_name = 'registration/register.html'
    if request.method == 'POST':
        reg_form = NewUserForm(request.POST)
        member_form = NewMemberForm(request.POST, request.FILES)

        if reg_form.is_valid():
            user = reg_form.save()
            member_group = Group.objects.get(name='Member')
            user.groups.add(member_group)
            user.save()
            profile = member_form.save(commit=False)
            profile.user = user
            if member_form.is_valid():
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
            profile.save()
            user = authenticate(username=profile.user.username, password=reg_form.cleaned_data.get('password2'))
            login(request, user)
            return redirect('/')
        return render(request, template_name, {'reg_form': reg_form, 'member_form': member_form})
    else:
        reg_form = NewUserForm()
        member_form = NewMemberForm()
    return render(request=request, template_name=template_name,
                  context={'reg_form': reg_form, 'member_form': member_form})


def login_page(request):
    template_name = 'registration/login.html'
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.blocked:
                    return redirect('/blocked/')
                login(request, user)
                return redirect('/')
    else:
        login_form = AuthenticationForm()
    return render(request=request, template_name=template_name, context={'login_form': login_form})


def logout_page(request):
    logout(request)
    return redirect('/')


def update_profile(request, username):
    user_page = get_object_or_404(User, username=username)
    profile = user_page.profile
    template = loader.get_template('update.html')
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)
    return HttpResponse(template.render({'profile_form': profile_form, 'user_form': user_form}, request))


def change_password(request, username):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(request.user, request.POST)
        if pass_form.is_valid():
            user = pass_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        pass_form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'pass_form': pass_form})


def blocked(request):
    template = loader.get_template('blocked.html')
    return HttpResponse(template.render({}, request))


class WarnUser(CheckMemberMixin, PostLastPage, generic.TemplateView):
    permission_required = "user_management.warn_member"
    template_name = 'warn-member.html'

    # Post executes the warning onto the user
    def post(self, request, *args, **kwargs):
        actions.warn_user(request, kwargs['pk'])
        return super().post(request, *args, **kwargs)

    # Sets the context data to include the user object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = actions.get_user(kwargs['pk'])
        context['object'] = user
        return context


# User flagging view handler (POST ONLY)
# Make sure that you have the ?next attribute in the POST header to take the user back to their last page
class FlagUser(CheckMemberMixin, PostLastPage, ActionView):
    permission_required = 'administration.add_userflag'

    def post(self, request, *args, **kwargs):
        actions.flag_user(request, kwargs['pk'])

        return super().post(request, *args, **kwargs)


# User blocking view handler (POST)
# Make sure that you have the ?next attribute in the POST header to take the user back to their last page
class BlockUser(CheckMemberMixin, PostLastPage, ActionView):
    permission_required = "user_management.block_member"

    def post(self, request, *args, **kwargs):
        actions.block_user(request, kwargs['pk'])

        return super().post(request, *args, **kwargs)


# User creation view for superuser
def AdminUserCreateView(request):
    template_name = 'create-member.html'
    if request.user.has_perm('user_management.add_member'):
        user_form = NewUserForm(request.POST)
        member_form = NewMemberForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            member_group = Group.objects.get(name='Member')
            user.groups.add(member_group)
            user.save()
            profile = member_form.save(commit=False)
            profile.user = user
            if member_form.is_valid():
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
            profile.save()
            return redirect('/useradmin')
        return render(request, template_name, {'user_form': user_form, 'member_form': member_form})
    else:
        return HttpResponseForbidden()


# A view for confirming the deletion of a user
# Make sure that you have the ?next attribute in the POST header to take the user back to their last page
class DeleteUserView(CheckMemberMixin, DeleteView, PostLastPage):
    permission_required = "user_management.delete_member"
    template_name = 'delete-member.html'
    model = User
    success_url = '/useradmin/'

    def post(self, request, *args, **kwargs):
        actions.delete_user(request, kwargs['pk'])

        return super().post(request, *args, **kwargs)


def notifs(request):
    template_name = 'notif.html'
    username = request.user.username
    user = User.objects.get(username=username)
    read(request)
    notif2 = user.notifications.read()
    return render(request, template_name, {'notif2': notif2})


def read(request):
    username = request.user.username
    user = User.objects.get(username=username)
    user.notifications.mark_all_as_read()
    return redirect('/notifications')
