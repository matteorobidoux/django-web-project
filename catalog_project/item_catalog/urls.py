from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import ItemCreateView, ItemListView, ItemEditView, ItemDeleteView, ItemDetailView, AddCommentView, LikeView, RateView

urlpatterns = [
    # Index page
    path('', ItemListView.as_view(), name="explore-projects"),
    path('project/new/', ItemCreateView.as_view(), name='new-project'),
    path('project/edit/<int:pk>', ItemEditView.as_view(), name='edit_project'),
    path('project/delete/<int:pk>', ItemDeleteView.as_view(), name='delete_project'),
    path('project/<int:pk>/', ItemDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/comment', AddCommentView.as_view(), name='project-comment'),
    path('like/<int:pk>', LikeView, name="like-project"),
    path('rate/<int:pk>', RateView, name="rate-project"), 
]