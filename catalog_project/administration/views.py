from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def dashboard(request):
    # Load template from templates/administration/dashboard.html
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render({}, request)) p