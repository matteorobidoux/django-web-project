from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def manage_users(request):
    template = loader.get_template('manage-users.html')
    return HttpResponse(template.render({}, request))
