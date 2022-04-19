from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages, name='messages')

    # Map a message id
    # path('message/<int:message_id>/', views.view_message, name="view_message"),
]