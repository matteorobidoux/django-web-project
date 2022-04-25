from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import redirect
from user_management.models import Warning, Profile

# Redirects you to page 1 when you open up the admin dashboard
def dashboard_redirect(request):
    return redirect('page/1')

# Main dashboard interface when you open the dashboard. Uses the page as an argument to filter users.
class Dashboard(generic.ListView):
    # Default model is user.
    model = User;
    context_object_name = 'user_list'
    template_name = 'dashboard.html'

    # Get the users based on the page given as an argument
    def get_queryset(self):
        page = self.kwargs["page"]
        start_users = 5*(page-1)
        end_users = 5*page
        return User.objects.all()[start_users:end_users]

# Dashboard functions
def warn_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        message = request.POST.get('warning-message')
        warning = Warning(message=message,user=user)
        warning.save()
    else:
        template = loader.get_template('warn-user.html')
        context = {
            'user': user
        }
        return HttpResponse(template.render(context, request))
    return redirect('/admin')


# Dashboard functions
def flag_user(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        profile.flagged = not profile.flagged
        profile.save()
    return redirect('/admin')

# Dashboard functions
def edit_user(request, id):
    if request.method == 'POST':
        print(f"Edited user {id}")
    return redirect('/admin')

# Dashboard functions
def delete_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.delete()
    else:
        template = loader.get_template('delete-user.html')
        context = {
            'user': user
        }
        return HttpResponse(template.render(context, request))
    return redirect('/admin')