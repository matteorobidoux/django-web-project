from django import forms
from .models import Rating, Comment, Item


# RateForm is to add ratings to a model
class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']
        exclude = ['user', 'item',]


# CommentForm is to add comments to a model
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        exclude = ['commenter', 'item']