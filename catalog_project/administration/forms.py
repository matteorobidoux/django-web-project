from django import forms
from django.contrib.auth.models import User, Group
from user_management.models import Profile
from user_management.user_form import NewUserForm

# A creation form for the user
class UserCreateForm(NewUserForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'groups')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
            # Add the users to the groups after a commit
            for groupName in self.cleaned_data['groups']:
                group = Group.objects.get(name=groupName)
                group.user_set.add(user)

        return user


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