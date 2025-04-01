from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title' : 'Home - Login'
    }
    return render(request, 'users/login.html', context=context)

def registration(request):
    context = {
        'title' : 'Home - Registration'
    }
    return render(request, 'users/registration.html', context=context)

def logout(request):
    pass
    context = {
        'title' : 'Home - Logout'
    }
    return render(request, 'users/logout.html', context=context)

def profile(request):
    context = {
        'title' : 'Home - Profile'
    }

    return render(request, 'users/profile.html', context=context)   