from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.generic import DetailView
from .models import Profile
from .user_form import NewUserForm, NewMemberForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import Group
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from administration.views import EditUserView


def manage_users(request):
    template = loader.get_template('manage-users.html')
    return HttpResponse(template.render({}, request))


def profile_page(request, username=None):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view profiles')
        return redirect('/login')
    template = loader.get_template('profile.html')
    if username:
        user_page = get_object_or_404(User, username=username)
        profile = user_page.profile
    else:
        user_page = request.user.username
        profile = request.user.profile
    return HttpResponse(template.render({'profile': profile, 'user': user_page}, request))


def register(request):
    template_name = 'registration/register.html'
    if request.method == 'POST':
        reg_form = NewUserForm(request.POST)
        member_form = NewMemberForm(request.POST, request.FILES)

        if reg_form.is_valid():
            user = reg_form.save()
            member_group = Group.objects.get(name='Member')
            user.groups.add(member_group)
            user.save()
            profile = member_form.save(commit=False)
            profile.user = user
            if member_form.is_valid():
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
            profile.save()
            user = authenticate(username=profile.user.username, password=reg_form.cleaned_data.get('password2'))
            login(request, user)
            return redirect('/')
        return render(request, template_name, {'reg_form': reg_form, 'member_form': member_form})
    else:
        reg_form = NewUserForm()
        member_form = NewMemberForm()
    return render(request=request, template_name=template_name, context={'reg_form': reg_form, 'member_form': member_form})


def login_page(request):
    template_name = 'registration/login.html'
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.blocked:
                    return redirect('/blocked/')
                login(request, user)
                return redirect('/')
    else:
        login_form = AuthenticationForm()
    return render(request=request, template_name=template_name, context={'login_form': login_form})


def logout_page(request):
    logout(request)
    return redirect('/')

def update_profile(request, username):
    user_page = get_object_or_404(User, username=username)
    profile = user_page.profile
    template = loader.get_template('update.html')
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)
    return HttpResponse(template.render({'profile_form': profile_form, 'user_form': user_form}, request))

def change_password(request, username):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(request.user, request.POST)
        if pass_form.is_valid():
            user = pass_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        pass_form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'pass_form': pass_form})

def blocked(request):
    template = loader.get_template('blocked.html')
    return HttpResponse(template.render({}, request))
