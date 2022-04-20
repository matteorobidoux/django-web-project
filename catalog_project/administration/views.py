from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Redirects you to page 1 when you open up the admin dashboard
def dashboard_redirect(request):
    return redirect('page/1')

# Main dashboard interface when you open the dashboard. Uses the page as an argument to filter users.
class Dashboard(generic.ListView):
    # Default model is user.
    model = User;
    context_object_name = "user_list"
    template_name = 'dashboard.html'

    # Get the users based on the page given as an argument
    def get_queryset(self):
        page = self.kwargs["page"]
        start_users = 5*(page-1)
        end_users = 5*page
        return User.objects.all()[start_users:end_users]

