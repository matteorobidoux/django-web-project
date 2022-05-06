from django.urls import path
from . import views


urlpatterns = [
    # User manager for user admins
    path('manage-users/', views.manage_users, name='manage_users'),
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
    # Profile update page
    path(r'profile/<str:username>/password', views.change_password, name="edit_password"),
    # User editing page
    # path('profile/edit/<int:pk>/', views.ManagerUserEditView.as_view(), name="manager_edit_user"),

    # Blocked user
    path('blocked/', views.blocked, name='blocked')
]