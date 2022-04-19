from django.urls import path
from . import views

urlpatterns = [
    # Index page
    path('index/', views.index, name="index"),
    path('', views.index, name="index"),

    # Explore projects
    #path('explore/', views.explore, name="explore_projects"),
    # View a project
    #path('explore/project/<int:project_id>/', views.project_view, name="view_project"),
    # Edit a project
    #path('explore/edit/<int:project_id>/', views.project_edit, name="edit_project"),
]