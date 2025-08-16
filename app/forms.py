from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from app.models import CustomUser, Motor, Advertisement

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

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

class AdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = ['motor', 'title', 'description']
        widgets = {
            'motor': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter advertisement title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the vehicle or sale terms'}),
        }
        labels = {
            'motor': 'Vehicle',
            'title': 'Advertisement Title',
            'description': 'Description',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['motor'].queryset = Motor.objects.filter(user__in=[user, None])
        

class MotorForm(ModelForm):
    class Meta:
        model = Motor
        fields = ['name', 'brand', 'model', 'description', 'price', 'power', 'made_at', 'mileage', 'condition', 'image']
        widgets = {
            'condition': forms.Select(choices=Motor.VEHICLE_CONDITION, attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., My Red Honda'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Honda'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Civic'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the vehicle'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 15000.00'}),
            'power': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'e.g., 50'}),
            'made_at': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2015'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50000'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Vehicle Name',
            'brand': 'Brand',
            'model': 'Model',
            'description': 'Description',
            'price': 'Price (EUR)',
            'power': 'Power (HP)',
            'made_at': 'Year Manufactured',
            'mileage': 'Mileage',
            'condition': 'Condition',
            'image': 'Vehicle Image',
        }
    