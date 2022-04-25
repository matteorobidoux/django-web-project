from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView

class ItemListView(ListView):
    model = Item
    template_name = 'item_catalog/explore.html'
    context_object_name = 'items'
    ordering = ['-date_posted']
    paginate_by = 5

class ItemCreateView(CreateView):
    model = Item
    success_url = '/'
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'item_catalog/new_project.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)