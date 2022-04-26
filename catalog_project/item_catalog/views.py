from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

class ItemListView(ListView):
    model = Item
    template_name = 'explore.html'
    context_object_name = 'items'
    ordering = ['-date_posted']
    paginate_by = 5

class ItemCreateView(CreateView):
    model = Item
    success_url = '/'
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'new_project.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Mostly used to return error responses
def response_not_found_404(request, exception):
    template = loader.get_template('response-404.html')
    return HttpResponseNotFound(template.render({}))
