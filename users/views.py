from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth
# Create your views here.
def login(request):

    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            password = request.POST['password']
            username = request.POST['username']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    context = {
        'title' : 'Home - Login',
        'form' : form

    }
    return render(request, 'users/login.html', context=context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()
     
    context = {
        'title' : 'Home - Registration',
        'form' : form
    }
    return render(request, 'users/registration.html', context=context)

def logout(request):
    auth.logout(request)
    
    return redirect(reverse('main:index'))
def profile(request):
    context = {
        'title' : 'Home - Profile'
    }

    return render(request, 'users/profile.html', context=context)   