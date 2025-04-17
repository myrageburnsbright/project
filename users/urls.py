
from django.urls import path

from users import views

app_name ='users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', views.logout, name='logout'),
    path('users_cart/', views.UserCartView.as_view(), name='users_cart'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
