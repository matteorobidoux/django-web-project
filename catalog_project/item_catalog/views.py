from django.shortcuts import render, get_object_or_404
from .models import Item, Comment
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, request, HttpResponseNotFound, request
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

class ItemEditView(UpdateView):
    model = Item
    success_url = '/'
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'edit_project.html'

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('explore-projects')
    template_name = 'delete_project.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'

class AddCommentView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'comment.html'
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.commenter = self.request.user
        obj.save
        return super().form_valid(form)

def LikeView(request, pk):
    item = get_object_or_404(Item, id=request.POST.get('item_id'))
    item.likes.add(request.user)
    return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))

# Mostly used to return error responses
def response_not_found_404(request, exception):
    template = loader.get_template('response-404.html')
    return HttpResponseNotFound(template.render({}))

