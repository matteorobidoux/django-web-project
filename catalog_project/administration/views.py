from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic, View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
import actions

# Redirects you to page 1 when you open up the admin dashboard
def dashboard_redirect(request):
    return redirect('page/1')

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

class EditUser(PermissionRequiredMixin, View):
    permission_required = "change_user"

    def post(self, request, *args, **kwargs):

        print(f"Edited user {id}")
        return redirect('/admin')

class DeleteUser(PermissionRequiredMixin, View):
    permission_required = "delete_user"

    # Post executes the deletion
    def delete(self, request, *args, **kwargs):
        actions.delete_user(request, kwargs['id'])
        return redirect('/admin')

    # Get shows the deletion confirmation page
    def get(self, request, *args, **kwargs):
        template = loader.get_template('delete-user.html')
        context = {
            'target_user': self.get_user(kwargs)
        }
        return HttpResponse(template.render(context, request))
