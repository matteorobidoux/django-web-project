from django.urls import path
from . import views


urlpatterns = [
    # User manager for user admins
    path('useradmin/', views.ManageUsers.as_view(), name='manage_users'),
    # Login page
    path(r'login/', views.login_page, name="login"),
    # Register page
    path(r'register/', views.register, name="register"),
    # Reset password page
    # path('reset-password/', views.reset_password, name="reset_password"),
    # Logout page
    path(r'logout', views.logout_page, name="login"),

    # User profile page
    path(r'profile/<str:username>/', views.profile_page, name="user_profile"),
    # User update page
    path(r'profile/<str:username>/edit', views.update_profile, name="edit_profile"),
    # Profile password page
    path(r'profile/<str:username>/password', views.change_password, name="edit_password"),

    # Warn user view
    path('useradmin/warn_user/<int:pk>/', views.WarnUser.as_view(), name="warn_member"),
    # Flag user view (POST)
    path('/useradmin/flag_user/<int:pk>/', views.FlagUser.as_view(), name="flag_member"),
    # Block user view (POST)
    path('useradmin/block_user/<int:pk>/', views.BlockUser.as_view(), name="block_member"),
    # Create user view
    path('useradmin/create/', views.AdminUserCreateView, name="create_member"),
    # Delete user view
    path('useradmin/delete_user/<int:pk>/', views.DeleteUserView.as_view(), name="delete_member"),
    # Blocked user
    path('blocked/', views.blocked, name='blocked'),
    # Notifications
    path('notifications/', views.notifs, name='notifications'),
    # Mark read
    path('notifications/mark-all-as-read/', views.read, name='read')
]