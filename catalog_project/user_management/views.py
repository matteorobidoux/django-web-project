from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Profile
from .user_form import NewUserForm, NewMemberForm


# Create your views here.


def manage_users(request):
    template = loader.get_template('manage-users.html')
    return HttpResponse(template.render({}, request))


def home(request):
    template = loader.get_template('profile.html')
    profile = request.user.profile
    return HttpResponse(template.render({'profile': profile}, request))


def register(request):
    template_name = 'registration/register.html'
    if request.method == 'POST':
        reg_form = NewUserForm(request.POST)
        member_form = NewMemberForm(request.POST, request.FILES)

        if reg_form.is_valid():
            user = reg_form.save()
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
                login(request, user)
                return redirect('/')
    else:
        login_form = AuthenticationForm()
    return render(request=request, template_name=template_name, context={'login_form': login_form})


def logout_page(request):
    logout(request)
    return redirect('/')




