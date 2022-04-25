from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

# Create your views here.
# Placeholder index html page for when you open the site.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

# Mostly used to return error responses
def response_not_found_404(request, exception):
    template = loader.get_template('response-404.html')
    return HttpResponseNotFound(template.render({}))