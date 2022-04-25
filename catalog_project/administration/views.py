from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic
from django.contrib.auth.models import User, Group
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
    max_per_page = 3

    def get_max_pages(self):
        return int(len(User.objects.all())/self.max_per_page)+1

    # Get the users based on the page given as an argument
    def get_queryset(self):
        page = self.kwargs["page"]
        start_users = self.max_per_page*(page-1)
        end_users = self.max_per_page*page
        return User.objects.all()[start_users:end_users]

    # Add extra context data such as a page
    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        page = self.kwargs["page"]
        context['page'] = page
        context['next_page'] = page+1
        context['last_page'] = page-1
        context['max_pages'] = self.get_max_pages()
        return context

    def dispatch(self, request, *args, **kwargs):
        issuer = request.user
        in_group = issuer.groups.filter(name="Superuser").exists()
        if not in_group:
            raise Http404("Page not found")

        page = self.kwargs["page"]
        max_pages = self.get_max_pages()
        if page < 1 or page > max_pages:
            page = 1 if page < 1 else page
            page = max_pages if page > max_pages else page
            return redirect(f'/admin/page/{page}')

        return super(Dashboard, self).dispatch(request, *args, **kwargs)

# Dashboard functions
def warn_user(request, id):
    issuer = request.user
    user = User.objects.get(id=id)
    if not issuer.has_perm('warn_user'):
        return Http404("Page not found")

    if request.method == "POST":
        message = request.POST.get('warning-message')
        warning = Warning(message=message,user=user)
        warning.save()
    else:
        template = loader.get_template('warn-user.html')
        context = {
            'target_user': user
        }
        return HttpResponse(template.render(context, request))
    return redirect('/admin')


# Dashboard functions
def flag_user(request, id):
    issuer = request.user
    if not issuer.has_perm('flag_user'):
        raise Http404("Page not found")

    if request.method == 'POST':
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        profile.flagged = not profile.flagged
        profile.save()
    return redirect('/admin')

# Dashboard functions
def edit_user(request, id):
    issuer = request.user
    if not issuer.has_perm('change_user'):
        raise Http404("Page not found")

    if request.method == 'POST':
        print(f"Edited user {id}")
    return redirect('/admin')

# Dashboard functions
def delete_user(request, id):
    issuer = request.user
    if not issuer.has_perm('delete_user'):
        raise Http404("Page not found")

    user = User.objects.get(id=id)
    if request.method == "POST":
        user.delete()
    else:
        template = loader.get_template('delete-user.html')
        context = {
            'target_user': user
        }
        return HttpResponse(template.render(context, request))
    return redirect('/admin')