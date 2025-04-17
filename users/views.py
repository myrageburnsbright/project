from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.db.models import Prefetch
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart
from users.models import User
# Create your views here.
class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    #success_url = reverse_lazy('main:index')
    def get_success_url(self):
        redirect_page = self.request.POST.get('next')
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                old_carts = Cart.objects.filter(user=user)
                if old_carts.exists():
                    old_carts.delete()
                
                Cart.objects.filter(session_key=session_key).update(user=user)
        
            messages.success(self.request, f"{user.username} вы вошли в аккаунт!")

            return redirect(self.get_success_url())

    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home - Login'  
        return context
    

class RegistrationView(CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.instance

        if user:
            form.save()
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            
            messages.success(self.request, f"{user.username} вы успешно зарегестрировались")
            return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Registration'
        return context

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
                    # delete old authorized user carts
                    forgot_carts = Cart.objects.filter(user=user)
                    if forgot_carts.exists():
                        forgot_carts.delete()
                     # add new authorized user carts from anonimous session
                    
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

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset = None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "при обновлении профайла произошла ошибка!")
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Profile'
        context['orders'] = orders = Order.objects.filter(user=self.request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("product")
        )
    ).order_by("-id")
        return context

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

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("product")
        )
    ).order_by("-id")

    context = {
        'title' : 'Home - Profile',
        'form' : form,
        'orders' : orders
    }
    return render(request, 'users/profile.html', context=context)

class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context


def users_cart(request):
    return render(request, 'users/users_cart.html')