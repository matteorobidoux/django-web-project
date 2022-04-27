from django.shortcuts import render
from .models import Item
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from django.http import HttpResponse, request, HttpResponseNotFound, request
from django.template import loader
from django.contrib.auth.models import User

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
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save
        return super().form_valid(form)

class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'

# Mostly used to return error responses
def response_not_found_404(request, exception):
    template = loader.get_template('response-404.html')
    return HttpResponseNotFound(template.render({}))
