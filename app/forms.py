from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from app.models import CustomUser

class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username = username, password = password)
            if user is None:
                raise forms.ValidationError("Invalid username od password!")
            self.user = user
        return cleaned_data
    
    
class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)
    username = forms.CharField(max_length=20, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    location = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "phone_number", "location", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")
        return password2
    
class AccountForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "phone_number", "location"]