from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import redirect

def dashboard_redirect(request):
    return redirect('page/1')

# Create your views here.
class Dashboard(generic.ListView):
    model = User;
    context_object_name = "user_list"
    template_name = 'dashboard.html'

    def get_queryset(self):
        page = self.kwargs["page"]
        start_users = 5*(page-1)
        end_users = 5*page
        return User.objects.all()[start_users:end_users]

