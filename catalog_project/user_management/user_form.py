from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile



# Create your forms here.

class NewUserForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewMemberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )
