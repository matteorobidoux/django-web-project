from django.urls import path
from . import views

urlpatterns = [
    # Full item view page
    path('items/', views.ItemViewSet.as_view(), name="item_api"),
    # View a specific item
    path('items/<int:pk>/', views.SingleItemViewSet.as_view(), name='item_view_api'),
    # Item managers or owners can edit/delete an item
    path('items/manage/<int:pk>/', views.ManageSingleItemViewSet.as_view(), name='item_manage_api'),
    # Create an item
    path('items/create/', views.CreateItemViewSet.as_view(), name='item_create_api')
]