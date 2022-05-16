from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.template import loader
from django.views import generic
from django.views.generic import DeleteView
from .user_form import NewUserForm, NewMemberForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import Group

from administration import actions
from administration.views import ActionView, PostLastPage, UserCreateView, ModelSearchListView, TargetUserView


# Uses has_permission mixin function to check if the action is being enacted on a member
class CheckMemberMixin(PermissionRequiredMixin, TargetUserView):
    def has_permission(self):
        if not self.target.groups.filter(name='Member').exists() or self.target.groups.all().count()>1 :
            return False

        return super().has_permission()


# Manage user dashboard for Member Admins
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


# Profile page view for a user
def profile_page(request, username=None):
    # Redirect user if they're not authenticated
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view profiles')
        return redirect('/login')
    template = loader.get_template('profile.html')

    # Get profile data based on if they're flagged
    profile = None
    if username:
        user_page = get_object_or_404(User, username=username)
        profile = user_page.profile
    else:
        user_page = request.user.username
        profile = request.user.profile

    # Throw a 404 if the user is flagged, and the requester is not an admin nor the profile user
    if profile.user != request.user and not request.user.has_perm('administration.add_userflag') and profile.flagged:
        raise Http404;

    return HttpResponse(template.render({'profile': profile, 'user': user_page}, request))


# Register view for new users
def register(request):
    template_name = 'registration/register.html'
    if request.method == 'POST':
        # Get forms for profile and suer
        reg_form = NewUserForm(request.POST)
        member_form = NewMemberForm(request.POST, request.FILES)
        # Check if valid
        if reg_form.is_valid():
            # Create user from registration form
            user = reg_form.save()
            member_group = Group.objects.get(name='Member')
            user.groups.add(member_group)
            user.save()
            # Get profile form
            profile = member_form.save(commit=False)
            profile.user = user
            # If the profile form is valid, save the profile
            if member_form.is_valid():
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
                profile.save()
                # Authenticate the user once they're created
                user = authenticate(username=profile.user.username, password=reg_form.cleaned_data.get('password2'))
                login(request, user)
                return redirect('/')
            else:
                # Remove the user if its invalid
                user.delete()
        return render(request, template_name, {'reg_form': reg_form, 'member_form': member_form})
    else:
        reg_form = NewUserForm()
        member_form = NewMemberForm()
    return render(request=request, template_name=template_name,
                  context={'reg_form': reg_form, 'member_form': member_form})


# Login page view
def login_page(request):
    template_name = 'registration/login.html'
    if request.method == 'POST':
        # Get the authentication form
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            # Checks if the data is cleaned
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # Check authentication
            user = authenticate(username=username, password=password)
            # Redirect if teh user is blocked
            if user is not None:
                if user.profile.blocked:
                    return redirect('/blocked/')
                # If not, they can log in
                login(request, user)
                return redirect('/')
    else:
        login_form = AuthenticationForm()
    return render(request=request, template_name=template_name, context={'login_form': login_form})


# Logout page view
def logout_page(request):
    logout(request)
    return redirect('/')


# Profile editing view for users
@login_required(login_url='/login/')
def update_profile(request, username):
    user_page = get_object_or_404(User, username=username)
    profile = user_page.profile
    template = loader.get_template('update.html')
    # Checks the post emethod
    if request.method == 'POST':
        # Get the forms
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        # Check if both are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save both forms and the profile
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')
    else:
        # Return new forms to render
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)
    return HttpResponse(template.render({'profile_form': profile_form, 'user_form': user_form}, request))


# Password change view
@login_required(login_url='/login/')
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


# Redirects the user to the blocked page if they're blocked
def blocked(request):
    template = loader.get_template('blocked.html')
    return HttpResponse(template.render({}, request))


# User warning action for User Manager
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


# User creation view for Member Admin
def admin_user_create(request):
    template_name = 'create-member.html'
    # Checks for permission
    if request.user.has_perm('user_management.add_member'):
        user_form = NewUserForm(request.POST)
        member_form = NewMemberForm(request.POST, request.FILES)
        # Check if the user form is valid
        if user_form.is_valid():
            # Creates the user and profile
            user = user_form.save()
            member_group = Group.objects.get(name='Member')
            user.groups.add(member_group)
            user.save()
            profile = member_form.save(commit=False)
            profile.user = user

            # Check if the profile form is valid
            if member_form.is_valid():
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
                profile.save()
                actions.create_user(request, user.id)
                return redirect('/useradmin')
            else:
                # Delete the user if the profile is invalid
                user.delete()
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

    # Logs the action
    def post(self, request, *args, **kwargs):
        actions.delete_user(request, kwargs['pk'])
        return super().post(request, *args, **kwargs)


# Shows all the notifications that a user has
@login_required(login_url='/login/')
def notifs(request):
    template_name = 'notif.html'
    username = request.user.username
    user = User.objects.get(username=username)
    read(request)
    notif2 = user.notifications.read()
    return render(request, template_name, {'notif2': notif2})


# Sets the notifications as "read"
@login_required(login_url='/login/')
def read(request):
    username = request.user.username
    user = User.objects.get(username=username)
    user.notifications.mark_all_as_read()
    return redirect('/notifications')
