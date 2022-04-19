# URLS:
# Main view for the website administration site
# Topbar view
# Template view for listing all of the users in a table
# Template view for the actions on a user
# A template view for the user themselves with additional information about them. Clicked on when they get on the page
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard view
    path('', views.dashboard, name="admin_board"),
    # User editor view
    #path('edit-user/<int:user_id>/', views.edit_user, name="edit_user"),
    # User creator view
    #path('create-user/', views.create_user, name="create_user"),
]