from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_users, name='manage_users')
]