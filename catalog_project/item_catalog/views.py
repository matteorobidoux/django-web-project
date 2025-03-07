from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, request, Http404)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.detail import SingleObjectMixin
from .forms import RateForm, CommentForm
from .models import Comment, Item, Rating
from administration import actions
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# View that redirects the user to the last page they were on upon POSTing
class PostLastPage:
    no_next_redirect = reverse_lazy('admin_board')

    # Post redirects you to 'next' if it exists
    def post(self, request, *args, **kwargs):
        next_page = request.POST.get('next', self.no_next_redirect)
        return HttpResponseRedirect(next_page)


# Defines a search filter for a list view
class ModelSearchListView(ListView):
    search_redirect = ''

    # Context data contains all the possible fields for an item
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['item_fields'] = self.sort_fields
        return context

    # Post handles the search query and redirects to a url with the query inside it
    def post(self, request, *args, **kwargs):
        search = request.POST.get('search-query', '')
        filter = request.POST.get('filter-by', '')

        filter_arg = f'filter={filter}' if filter else ''
        search_arg = f'search={search}' if search else ''

        appended = f'?{filter_arg}&{search_arg}' if filter_arg and search_arg else ''

        return redirect(f'{self.search_redirect}/{appended}')

    # Gets all the filterable attributes from the GET request
    def get_filter_attributes(self):
        search = self.request.GET.get('search')
        filter = self.request.GET.get('filter')

        return search, filter

    # Gets the filtered result using the GET request search filter attributes
    def get_filter(self, queryset):
        search, filter = self.get_filter_attributes()

        field_names = [ field.name for field in self.model._meta.get_fields()]
        if filter in field_names:
            kwargs = {
                f'{filter}__istartswith': search
            }
            if filter and search:
                queryset = queryset.filter(**kwargs)

        return queryset

    # Gets the queryset based on the search filter or keywords
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.get_filter(queryset)

        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(keyword_list__icontains=keyword)
        return queryset


# List View with search filter for Items (explore page)
class ItemListView(ModelSearchListView):
    search_redirect = ''

    sort_fields = ('name', 'status', 'type', 'field', 'owner', 'average rate')
    model = Item
    template_name = 'explore.html'
    context_object_name = 'items'
    ordering = ['-date_posted']
    paginate_by = 5

    # Defines a filter name for filtering by owner
    def get_filter_attributes(self):
        search, filter = super().get_filter_attributes()
        if filter == 'owner':
            filter = 'owner__username'
        return search, filter

    # Allows for filtering by owner and rate yields different results from regular filter
    def get_filter(self, queryset):
        search, filter = self.get_filter_attributes()
        queryset = super().get_filter(queryset)

        # If they're searching by username, then it looks inside the owner and the username
        if filter == "owner__username":
            queryset = queryset.filter(owner__username__icontains=search)
        # Uses annotate to filter rates by average
        elif filter == "average rate":
            queryset = queryset.annotate(average_rate=Avg('rating__rate')).filter(average_rate__startswith=search)
        return queryset

    # Gets the queryset and excludes flagged items
    def get_queryset(self):
        queryset = super().get_queryset()

        # Exclude flags if they're not a superuser
        if not self.request.user.has_perm('item_catalog.add_itemflag'):
            if not self.request.user.is_anonymous:
                # Don't exclude if the requester is the owner
                queryset = queryset.exclude(~Q(owner=self.request.user), flagged=True)
            else:
                queryset = queryset.exclude(flagged=True)

        return queryset


# The form for creating the item
class ItemCreateView(CreateView):
    model = Item
    success_url = '/'
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'new_project.html'

    # Automatically sets the owner as the user for the form
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


# Item Editing view for Item Admins
class ItemManageEditView(PermissionRequiredMixin, UpdateView):
    permission_required = "item_catalog.change_item"
    model = Item
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'edit_project.html'

    # Take the user to the item page
    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.pk})

    # Logs the request
    def post(self, request, *args, **kwargs):
        actions.edit_item(request,  kwargs['pk'])
        return super().post(request, *args, **kwargs)


# Item Delete view for Item Admins
class ItemManageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "item_catalog.delete_item"
    model = Item
    success_url = reverse_lazy('explore-projects')
    template_name = 'delete_project.html'

    # Logs the request
    def post(self, request, *args, **kwargs):
        actions.delete_item(request, kwargs['pk'])
        return super().post(request, *args, **kwargs)


# Item Flag view for Item Admins
class ItemManageFlagView(PermissionRequiredMixin, View, PostLastPage):
    permission_required = 'item_catalog.add_itemflag'

    # Logs the flag
    def post(self, request, *args, **kwargs):
        actions.flag_item(request, kwargs['pk'])
        return super().post(request, *args, **kwargs)


# Mixin for self auditing
class SelfAuditMixin(SingleObjectMixin):
    def get_object(self, queryset=None):
        object = super().get_object()
        if object:
            if self.request.user.id == object.owner.id:
                return object
            else:
                raise Http404


# Self audit Item Editing view for members
class ItemEditView(SelfAuditMixin, UpdateView):
    model = Item
    fields = ['name', 'type', 'field', 'keyword_list', 'content', 'status', 'url', 'snapshot']
    template_name = 'edit_project.html'

    # Takes the user to the item detail when they're done
    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.pk})


# Self audit Item Deletion view for members
class ItemDeleteView(SelfAuditMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('explore-projects')
    template_name = 'delete_project.html'


# Item detail view
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'item_detail.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        # Return 404 if the object is flagged and the user is neither the owner nor an admin
        if (self.get_object().flagged and
                not request.user.has_perm('item_catalog.add_itemflag') and
                request.user != self.get_object().owner):
            raise Http404
        return super().get(request, *args, **kwargs)


# View for adding comments to an item
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
            form = CommentForm(request.POST)
            # Check if the comment is valid
            if form.is_valid():
                # Create the comment and data related to it
                data = Comment()
                data.content = form.cleaned_data['content']
                data.commenter = self.request.user
                data.item = Item.objects.get(pk=self.kwargs['pk'])
                data.save()
                return redirect('project-detail', pk=self.kwargs['pk'])
            else:
                # Redirect the user if the form fails
                return redirect('project-detail', pk=self.kwargs['pk'])


# A view for adding likes to a post
@login_required(login_url='/login/')
def LikeView(request, pk):
    # Accept only POST requests
    if request.method == "POST":
        item = get_object_or_404(Item, id=pk)
        item.likes.add(request.user)
        return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))
    raise Http404;


# A view for rating a post
@login_required(login_url='/login/')
def RateView(request, pk):
    if request.method == 'POST':
        try:
            # Tries to create a rating
            ratings = Rating.objects.get(user__id=request.user.id, item__id=pk)
            form = RateForm(request.POST, instance=ratings)
            form.save()
            return HttpResponseRedirect(reverse('project-detail', args=[str(pk)]))
        except:
            # If there's an issue, then check if the form is valid and save that way
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


# Used to return 404 responses
def response_not_found_404(request, exception):
    template = loader.get_template('response-404.html')
    return HttpResponseNotFound(template.render({}))

