from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


# New User form for registering
class NewUserForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    # Cleans the email data
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# New Member form for Member Admins
class NewMemberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )


# Self audit User update form
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


# Self audit Profile update form
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )