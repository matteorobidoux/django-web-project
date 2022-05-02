from django import forms
from django.contrib.auth.models import User
from user_management.models import Profile
from user_management.user_form import NewUserForm

# A creation form for the user
class UserCreateForm(NewUserForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'groups')

# An update form for the user
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'groups')


# A generic form for the profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'flagged', 'blocked')