from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout, login as auth_login, authenticate
from .forms import AuthenticationForm, UserForm, AccountForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

# Create your views here.
def home(request):
    return render(request, "app/home.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('app:profile', user_id = user.id)
            else:
                form.add_error(None, "Invalid email or password!")
    
    else:
        form = AuthenticationForm()

    return render(request, 'app/login.html', {'form' : form})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('app:login')
    else:
        form = UserForm()

    return render(request, 'app/register.html', {"form" : form})

def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'app/profile.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('app:home')