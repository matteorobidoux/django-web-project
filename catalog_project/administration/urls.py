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
    path('', views.Dashboard.as_view(), name="admin_board"),
    path('warn_user/<int:id>/', views.WarnUser.as_view(), name="warn_user"),
    path('delete_user/<int:id>/', views.DeleteUser.as_view(), name="delete_user"),
    path('flag_user/<int:id>/', views.FlagUser.as_view(), name="flag_user"),
    path('block_user/<int:id>/', views.BlockUser.as_view(), name="block_user"),

    path('edit/<int:user_id>/', views.EditUserView.as_view(), name="admin_edit_user"),
    path('create/', views.UserCreateView.as_view(success_url="/admin/"), name="admin_create_user"),
    # User editor view
    #path('edit-user/<int:user_id>/', views.edit_user, name="edit_user"),
    # User creator view
    #path('create-user/', views.create_user, name="create_user"),
]