from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import ItemCreateView, ItemListView, ItemEditView, ItemDeleteView, ItemDetailView, AddCommentView, LikeView, RateView, ItemManageEditView, ItemManageDeleteView, ItemManageFlagView

urlpatterns = [
    # Explore view
    path('', ItemListView.as_view(), name="explore-projects"),
    # New project view
    path('project/new/', ItemCreateView.as_view(), name='new-project'),
    # Manager edit view
    path('project/manage_edit/<int:pk>', ItemManageEditView.as_view(), name='edit_project'),
    # Manager delete view
    path('project/manage_delete/<int:pk>', ItemManageDeleteView.as_view(), name='delete_project'),
    # Manager flag view
    path('project/manage_flag/<int:pk>', ItemManageFlagView.as_view(), name='flag_project'),
    # Self Edit view
    path('project/edit/<int:pk>', ItemEditView.as_view(), name='edit_own_project'),
    # Self Delete view
    path('project/delete/<int:pk>', ItemDeleteView.as_view(), name='delete_own_project'),
    # Detail view
    path('project/<int:pk>/', ItemDetailView.as_view(), name='project-detail'),
    # Comment view
    path('project/<int:pk>/comment', AddCommentView.as_view(), name='project-comment'),
    # Like view
    path('like/<int:pk>', LikeView, name="like-project"),
    # Rate view
    path('rate/<int:pk>', RateView, name="rate-project"), 
]