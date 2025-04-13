from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart
# Create your views here.
def login(request):

    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            password = request.POST['password']
            username = request.POST['username']
            user = auth.authenticate(username=username, password=password)
            
            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(request, f"{user.username} вы успешно зашли в аккаунт")
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout') :
                    return HttpResponseRedirect(redirect_page)
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
            session_key = request.session.session_key
            
            new_user = form.save()

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=new_user)

            messages.success(request, f"{new_user.username} вы успешно зарегестрировались")
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()
     
    context = {
        'title' : 'Home - Registration',
        'form' : form
    }
    return render(request, 'users/registration.html', context=context)
@login_required
def logout(request):
    auth.logout(request)
    
    messages.success(request, f"вы успешно вышли")
    return redirect(reverse('main:index'))

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data = request.POST, instance = request.user, files = request.FILES) 
        if form.is_valid():

            form.save()
            messages.success(request, f"Профиль успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else: 
        form = ProfileForm(instance = request.user)
     
    context = {
        'title' : 'Home - Profile',
        'form' : form
    }
    return render(request, 'users/profile.html', context=context)

def users_cart(request):
    return render(request, 'users/users_cart.html')