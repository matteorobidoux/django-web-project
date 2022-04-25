from django.urls import path
from . import views
from .views import ItemCreateView, ItemListView

urlpatterns = [
    # Index page
    path('', ItemListView.as_view(), name="explore-projects"),
    path('project/new/', ItemCreateView.as_view(), name='new-project'),

    # Explore projects
    #path('explore/', views.explore, name="explore_projects"),
    # View a project
    #path('explore/project/<int:project_id>/', views.project_view, name="view_project"),
    # Edit a project
    #path('explore/edit/<int:project_id>/', views.project_edit, name="edit_project"),
]