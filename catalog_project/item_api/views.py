import django_filters
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from item_catalog.models import Item
from .serializers import ItemSerializer

"""
Through well-defined urls (and query strings), users can use web API to:
a. list all items, specific items,
b. list or a single item.
c. update / delete items [your instructor may remove this requirement].

"""

# Viewset for viewing all items. You can filter by id,
class ItemViewSet(LoginRequiredMixin, generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'name', 'owner', 'type', 'field', 'status', 'date_posted']
    ordering_fields = ['id', 'name', 'owner', 'date_posted']
    ordering = ['name']


# Viewset for viewing a single item. Requires login, but no admin permissions.
class SingleItemViewSet(LoginRequiredMixin, generics.RetrieveAPIView):
    queryset = Item.objects.all()
    lookup_field = 'pk'
    serializer_class = ItemSerializer


# Viewset for managing an item. Checks if you can delete and change the item.
class ManageSingleItemViewSet(PermissionRequiredMixin, SingleItemViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    permission_required = ('delete_item', 'change_item')