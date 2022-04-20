from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
# Placeholder index html page for when you open the site.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))