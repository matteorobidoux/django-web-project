from django.urls import path
from . import views

urlpatterns = [
    # Index page
    path('items/', views.ItemViewSet.as_view(), name="item_api"),
    path('items/<int:pk>/', views.SingleItemViewSet.as_view(), name='item_view_api'),
    path('items/manage/<int:pk>/', views.ManageSingleItemViewSet.as_view(), name='item_manage_api')
]