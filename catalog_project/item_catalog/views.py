from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, request, Http404)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.detail import SingleObjectMixin

from .forms import RateForm
from .models import Comment, Item, Rating
from django.contrib.auth.mixins import PermissionRequiredMixin

class ModelSearchListView(ListView):
    search_redirect = ''
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['item_fields'] = self.sort_fields
        return context

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search-query', '')
        filter = request.POST.get('filter-by', '')

        filter_arg = f'filter={filter}' if filter else ''
        search_arg = f'search={search}' if search else ''

        appended = f'?{filter_arg}&{search_arg}' if filter_arg and search_arg else ''

        return redirect(f'{self.search_redirect}/{appended}')

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        filter = self.request.GET.get('filter')
        field_names = [ field.name for field in self.model._meta.get_fields()]
        if filter in field_names:
            kwargs = {
                f'{filter}__contains': search
            }
            if filter and search:
                queryset = queryset.filter(**kwargs)

        return queryset


class ItemListView(ModelSearchListView):
    search_redirect = ''

    sort_fields = ('name', 'status', 'type', 'field')
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

class ItemManageEditView(PermissionRequiredMixin, UpdateView):
    permission_required = "item_catalog.change_item"
    model = Item
    success_url = '/'
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'edit_project.html'

class ItemManageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "item_datalog.delete_item"
    model = Item
    success_url = reverse_lazy('explore-projects')
    template_name = 'delete_project.html'

class SelfAuditMixin(SingleObjectMixin):
    def get_object(self, queryset=None):
        object = super().get_object()
        if object:
            if self.request.user.id == object.owner.id:
                return object
            else:
                raise Http404


class ItemEditView(SelfAuditMixin, UpdateView):
    model = Item
    success_url = '/'
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'edit_project.html'


class ItemDeleteView(SelfAuditMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('explore-projects')
    template_name = 'delete_project.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'

    def post(self, request, *args, **kwargs):
        if request.user.id == self.object.owner.id:
            super().post(request, *args, **kwargs)
        return

class AddCommentView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'comment.html'
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.commenter = self.request.user
        obj.item_id = self.kwargs['pk']
        obj.save()
        return super().form_valid(form)

def LikeView(request, pk):
    item = get_object_or_404(Item, id=pk)
    print(item)
    item.likes.add(request.user)
    return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))

def RateView(request, pk):
    if request.method == 'POST':
        try:
            ratings = Rating.objects.get(user__id=request.user.id, item__id=pk)
            form = RateForm(request.POST, instance=ratings)
            form.save()
            return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))
        except:
            form = RateForm(request.POST)
            if form.is_valid():
                data = Rating()
                data.rate = form.cleaned_data['rate']
                data.item_id = pk
                data.user_id = request.user.id
                data.save()
                return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))
            else:
                return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))

# Mostly used to return error responses
def response_not_found_404(request, exception):
    template = loader.get_template('response-404.html')
    return HttpResponseNotFound(template.render({}))

