from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def manage_users(request):
    template = loader.get_template('manage-users.html')
    return HttpResponse(template.render({}, request))

def home(request):
    template_name = 'home.html'
    member = Profile.objects.get
    return HttpResponse(template.render({}, request))

def register(request):
    template_name = 'registration/register.html'
    if (request.method == 'POST'):
        reg_form = UserCreationForm(request.POST)

        if(reg_form.is_valid()):
            user = reg_form.cleaned_data.get('username')
            reg_form.save()
            messages.success(request, f'Registration successful for {user}.')
            return redirect('/login/')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        reg_form = UserCreationForm()
    return render(request=request, template_name=template_name, context={'reg_form':reg_form})

def login_page(request):
    template_name = 'registration/login.html'
    if (request.method == 'POST'):
        login_form = AuthenticationForm(request, data=request.POST)
        if (login_form.is_valid()):
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if (user is not None):
                login(request, user)
                return redirect('/')
    else:
        login_form = AuthenticationForm()
    return render(request=request, template_name=template_name, context={'login_form': login_form})

def logout_page(request):
    logout(request)
    return redirect('/')