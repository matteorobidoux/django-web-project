from django.urls import path
from . import views
from .views import ConvoList, CreateConvo, MessageList, CreateMessage

urlpatterns = [
    # List the conversations between users
    path('', ConvoList.as_view(), name='inbox'),
    # Creates a conversation with a new user
    path('create-convo/', CreateConvo.as_view(), name='create-convo'),
    # Views the message interaction between users
    path('<int:pkr>&<int:pks>/', MessageList.as_view(), name='messages'),
    # Creates a message for a new user
    path('<int:pkr>&<int:pks>/create-message', CreateMessage.as_view(), name='create-message'),
]