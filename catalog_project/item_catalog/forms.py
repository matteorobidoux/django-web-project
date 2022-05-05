from django import forms
from .models import Rating, Comment

class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']
        exclude = ['user', 'item',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        exclude = ['commenter', 'item']