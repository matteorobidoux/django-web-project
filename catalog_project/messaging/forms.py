from django import forms
from .models import Message


# A form for creating messages
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        exclude = ['sender', 'receiver']
