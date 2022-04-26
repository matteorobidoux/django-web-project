from django.urls import path
from . import views

urlpatterns = [
    # User manager for user admins
    path('manage-users/', views.manage_users, name='manage_users'),
    path('logout/', views.logout_user, name='logout'),
    # Login page
    #path('login/', views.login, name="login"),
    # Register page
    #path('register/', views.register, name="register"),
    # Reset password page
    #path('reset-password/', views.reset_password, name="reset_password"),

    # User profile page
    #path('user/<int:user_id>/', views.user_profile, name="user_profile"),
]