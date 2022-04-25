# URLS:
# Main view for the website administration site
# Topbar view
# Template view for listing all of the users in a table
# Template view for the actions on a user
# A template view for the user themselves with additional information about them. Clicked on when they get on the page
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect),
    # Dashboard view
    path('page/<int:page>/', views.Dashboard.as_view(), name="admin_board"),
    path('warn_user/<int:id>/', views.warn_user, name="warn_user"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),
    path('flag_user/<int:id>/', views.flag_user, name="flag_user"),
    path('edit_user/<int:id>/', views.edit_user, name="edit_user"),

    # User editor view
    #path('edit-user/<int:user_id>/', views.edit_user, name="edit_user"),
    # User creator view
    #path('create-user/', views.create_user, name="create_user"),
]