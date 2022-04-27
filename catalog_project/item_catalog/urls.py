from django.urls import path
from . import views
from .views import ItemCreateView, ItemListView, ItemEditView, ItemDeleteView

urlpatterns = [
    # Index page
    path('', ItemListView.as_view(), name="explore-projects"),
    path('project/new/', ItemCreateView.as_view(), name='new-project'),
    path('project/edit/<int:pk>', ItemEditView.as_view(), name='edit_project'),
    path('project/delete/<int:pk>', ItemDeleteView.as_view(), name='delete_project'),
]