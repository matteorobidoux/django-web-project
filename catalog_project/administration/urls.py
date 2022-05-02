from django.urls import path
from . import views

urlpatterns = [
    # Dashboard view
    path('', views.Dashboard.as_view(), name="admin_board"),
    # Logs view
    path('logs/', views.LogView.as_view(), name="logs"),
    # Warn user view
    path('warn_user/<int:pk>/', views.WarnUser.as_view(), name="warn_user"),
    # Flag user view (POST)
    path('flag_user/<int:pk>/', views.FlagUser.as_view(), name="flag_user"),
    # Block user view (POST)
    path('block_user/<int:pk>/', views.BlockUser.as_view(), name="block_user"),

    # Edit user view
    path('edit/<int:pk>/', views.AdminUserEditView.as_view(), name="admin_edit_user"),
    # Create user view
    path('create/', views.AdminUserCreateView.as_view(success_url="/admin/"), name="admin_create_user"),
    # Delete user view
    path('delete_user/<int:pk>/', views.DeleteUserView.as_view(), name="delete_user"),
]