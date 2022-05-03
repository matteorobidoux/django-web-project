from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import actions
from .forms import UserUpdateForm, ProfileForm, UserCreateForm
from django.views.generic.edit import CreateView, DeleteView
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.admin.models import LogEntry
from item_catalog.views import ModelSearchListView

""" Generic User management views """


# View that redirects the user to the last page they were on upon POSTing
class PostLastPage:
    no_next_redirect = reverse_lazy('admin_board')

    # Post redirects you to 'next' if it exists
    def post(self, request, *args, **kwargs):
        next_page = request.POST.get('next', self.no_next_redirect)
        return HttpResponseRedirect(next_page)


# A view for confirming the deletion of a user
# Make sure that you have the ?next attribute in the POST header to take the user back to their last page
class DeleteUserView(PermissionRequiredMixin, DeleteView, PostLastPage):
    permission_required = "auth.delete_user"
    template_name = 'delete-user.html'
    model = User
    success_url = PostLastPage.no_next_redirect

    def post(self, request, *args, **kwargs):
        actions.delete_user(request, kwargs['pk'])

        return super().post(request, *args, **kwargs)


# A view for editing the user
# Make sure that you have the ?next attribute in the POST header to take the user back to their last page
class EditUserView(PermissionRequiredMixin, PostLastPage, generic.TemplateView):
    user_form_model = UserUpdateForm
    profile_form_model = ProfileForm
    success_url = reverse_lazy('admin_board')

    # Getting initial data involves the two dictionaries representing the data inside the user and profile.
    def get_initial_data(self, kwargs):
        user = User.objects.get(id=kwargs['pk'])
        user_dict = model_to_dict(user)
        profile_dict = model_to_dict(user.profile)
        initial_user = { k: user_dict[k] for k in self.initial_user }
        initial_profile = { k: profile_dict[k] for k in self.initial_profile }
        return initial_user, initial_profile

    # Getting context involves getting the target user and the two forms for them
    def get_context_data(self, **kwargs):
        # Get user and initial data
        user = User.objects.get(id=kwargs['pk'])
        initial_user, initial_profile = self.get_initial_data(kwargs)
        # Create forms based on initial data
        user_form = self.user_form_model(instance=user, initial=initial_user)
        profile_form = self.profile_form_model(instance=user.profile, initial=initial_profile)
        # Set context
        context = super().get_context_data(**kwargs)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        context['object'] = user
        return context

    # Post saves the edits on the user and profile
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        user_form = self.user_form_model(request.POST, instance=user)
        profile_form = self.profile_form_model(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile has been updated")
            actions.edit_user(request, user.id)
            next_page = request.POST.get('next', '/')
            return HttpResponseRedirect(next_page)


# A view for creating a User
class UserCreateView(PermissionRequiredMixin, generic.TemplateView):
    user_form_model = UserCreateForm
    profile_form_model = ProfileForm
    success_url = reverse_lazy('admin_board')

    # Getting context involves getting the target user and the two forms for them
    def get_context_data(self, **kwargs):
        # Create forms based on initial data
        user_form = self.user_form_model()
        profile_form = self.profile_form_model()
        # Set context based on two forms
        context = super().get_context_data(**kwargs)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return context

    # Post saves the edits on the user and profile
    def post(self, request, *args, **kwargs):
        user_form = self.user_form_model(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save()
            profile_form = self.profile_form_model(request.POST, request.FILES, instance=user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "User has been created")
                return redirect(self.success_url)
            else:
                user.delete()
                messages.error(request, "User could not be created.")
                return redirect('')


""" Main pages """


# Main dashboard interface when you open the dashboard. Uses the page as an argument to filter users.
class Dashboard(PermissionRequiredMixin, ModelSearchListView):
    search_redirect = '/admin'
    sort_fields = ('id', 'username', 'email')
    permission_required = 'administration.view_dashboard'
    # Default model is user.
    model = User
    context_object_name = 'user_list'
    template_name = 'dashboard.html'
    ordering = ['id']
    paginate_by = 10
    def get(self, request, *args, **kwargs):
        print(request.user.get_user_permissions())
        return super().get(request, *args, **kwargs)

    # Adds the admin logs to the context data
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['logs'] = LogEntry.objects.all()[:10]
        return context


class LogView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'administration.view_dashboard'
    model = LogEntry
    context_object_name = 'logs'
    template_name = 'logs.html'
    ordering = ['-action_time']
    paginate_by = 20


""" Dashboard functions """


# Class for returning a 404 for GET requests because django doesnt already???
class ActionView(View):
    def get(self, request, *args, **kwargs):
        raise Http404


# The user warning view (POST AND GET)
class WarnUser(PermissionRequiredMixin, PostLastPage, generic.TemplateView):
    permission_required = "user_management.add_warning"
    template_name = 'warn-user.html'

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
class FlagUser(PermissionRequiredMixin, PostLastPage, ActionView):
    permission_required = 'administration.flag_user'

    def post(self, request, *args, **kwargs):
        actions.flag_user(request, kwargs['pk'])

        return super().post(request, *args, **kwargs)


# User blocking view handler (POST)
# Make sure that you have the ?next attribute in the POST header to take the user back to their last page
class BlockUser(PermissionRequiredMixin, PostLastPage, ActionView):
    permission_required = "administration.block_user"

    def post(self, request, *args, **kwargs):
        actions.block_user(request, kwargs['pk'])

        return super().post(request, *args, **kwargs)


# User editing view for superuser
class AdminUserEditView(EditUserView):
    success_url = reverse_lazy('admin_board')

    permission_required = 'auth.change_user'
    template_name = 'edit-user.html'
    initial_user = ('username', 'email')
    initial_profile = ('image', 'flagged', 'blocked')


# User creation view for superuser
class AdminUserCreateView(UserCreateView):
    success_url = reverse_lazy('admin_board')

    permission_required = "auth.add_user"
    template_name = 'create-user.html'





