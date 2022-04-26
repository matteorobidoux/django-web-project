from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic, View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from user_management.models import Warning, Profile
from django.contrib.auth.mixins import PermissionRequiredMixin

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

# View that checks for the permission
class AuthView(PermissionRequiredMixin, View):
    # Gets the user object based on kwargs
    def get_user(self, kwargs):
        return User.objects.get(id=kwargs["id"])

# The user warning view
class WarnUser(AuthView):
    permission_required = "warn_user"

    # Post executes the warning onto the user
    def post(self, request, *args, **kwargs):
        message = request.POST.get('warning-message')
        warning = Warning(message=message,user=self.get_user(kwargs))
        warning.save()
        return redirect('/admin')

    # Get shows the warning form page
    def get(self, request, *args, **kwargs):
        template = loader.get_template('warn-user.html')
        context = {
            'target_user': self.get_user(kwargs)
        }
        return HttpResponse(template.render(context, request))

class FlagUser(AuthView):
    permission_required = "flag_user"
    def post(self, request, *args, **kwargs):
        self.check_auth(request)
        user = self.get_user(kwargs)
        profile = Profile.objects.get(user=user)

        profile.flagged = not profile.flagged
        profile.save()
        return redirect('/admin')

class BlockUser(AuthView):
    permission_required = "flag_user"
    def post(self, request, *args, **kwargs):
        self.check_auth(request)
        user = self.get_user(kwargs)
        profile = Profile.objects.get(user=user)

        profile.blocked = not profile.blocked
        profile.save()
        return redirect('/admin')

class EditUser(AuthView):
    permission_required = "change_user"

    def post(self, request, *args, **kwargs):
        self.check_auth(request)

        print(f"Edited user {id}")
        return redirect('/admin')

class DeleteUser(AuthView):
    permission_required = "delete_user"

    # Post executes the deletion
    def post(self, request, *args, **kwargs):
        self.check_auth(request)
        user = self.get_user(kwargs)
        user.delete()
        print(f"Deleted {user}")
        return redirect('/admin')

    # Get shows the deletion confirmation page
    def get(self, request, *args, **kwargs):
        self.check_auth(request)

        template = loader.get_template('delete-user.html')
        context = {
            'target_user': self.get_user(kwargs)
        }
        return HttpResponse(template.render(context, request))
