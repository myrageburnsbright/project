
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm, UserCreationForm
from users.models import User

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    # username = forms.CharField()
    # password = forms.CharField()
    # username = forms.CharField(
    #     label = 'Имя',
    #     widget=forms.TextInput(attrs={'autofocus':True,
    #                                   'class':'form-control',
    #                                   'placeholder':'Введите ваше имя пользователя'})                                      
    # )
    # password = forms.CharField(
    #     label = 'Пароль',
    #     widget=forms.TextInput(attrs={'autofocus':True,
    #                                   'class':'form-control',
    #                                   'placeholder':'Введите ваш пароль'})                                      
    # )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    first_name = forms.CharField()
    last_name= forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()           

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'image']
        
    first_name = forms.CharField()
    last_name= forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    image = forms.ImageField(required=False)
