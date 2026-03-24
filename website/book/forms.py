from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        exclude = ['slug']
        
        
class GenereForm(ModelForm):
    class Meta:
        model = Genere
        exclude = ['slug']
        
        
class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['slug']
        

class RegisterForm(ModelForm, forms.Form):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {"password":forms.PasswordInput(render_value=False)}
        
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
