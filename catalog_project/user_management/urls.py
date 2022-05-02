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
    # path('user/<int:user_id>/', views.user_profile, name="user_profile"),
    path(r'profile/<str:username>/', views.profile_page, name="user_profile"),

    path(r'profile/', views.register, name="profile"),
    path('blocked/', views.blocked, name='blocked')
]