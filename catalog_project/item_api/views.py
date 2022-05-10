import django_filters
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from item_catalog.models import Item
from .serializers import ItemSerializer

# Viewset for viewing all items. You can filter by id,
class ItemViewSet(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'name', 'owner', 'type', 'field', 'status', 'date_posted']
    ordering_fields = ['id', 'name', 'owner', 'date_posted']
    ordering = ['id']


# Viewset for creating an item
class CreateItemViewSet(LoginRequiredMixin, generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


# Viewset for viewing a single item. Requires login, but no admin permissions.
class SingleItemViewSet(LoginRequiredMixin, generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Item.objects.all()
    lookup_field = 'pk'
    serializer_class = ItemSerializer


# Viewset for managing an item. Checks if you can delete and change the item.
class ManageSingleItemViewSet(UserPassesTestMixin, SingleItemViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def test_func(self):
        object = self.get_object()
        if self.request.user.has_perm('item_catalog.delete_item') or self.request.user.has_perm('item_catalog.change_item'):
            return True
        return object.owner == self.request.user