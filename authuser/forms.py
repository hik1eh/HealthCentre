from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

USER_TYPE = (
    ('Doctor', 'Доктор'),
    ('Pacient', 'Пациент'),
)

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@emailll.ru'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2', 'user_type']

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@emailll.ru'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ['email', 'password']



