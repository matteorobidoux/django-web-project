from django.urls import path
from . import views
from .views import ConvoList, CreateConvo, MessageList

urlpatterns = [
    path('', ConvoList.as_view(), name='inbox'),
    path('create-convo/', CreateConvo.as_view(), name='create-convo'),
    path('<int:pkr>&<int:pks>/', MessageList.as_view(), name='messages')

    # Map a message id
    # path('message/<int:message_id>/', views.view_message, name="view_message"),
]