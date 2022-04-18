# URLS:
# Main view for the website administration site
# Topbar view
# Template view for listing all of the users in a table
# Template view for the actions on a user
# A template view for the user themselves with additional information about them. Clicked on when they get on the page
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="admin_board")
]