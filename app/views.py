from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout, login as auth_login, authenticate
from .forms import AuthenticationForm, UserForm, AccountForm, AdvertisementForm, MotorForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Motor, Advertisement
from django.http import HttpResponse

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
    user = get_object_or_404(CustomUser, id=user_id)
    advertisements = Advertisement.objects.filter(user=request.user)
    return render(request, 'app/profile.html', {
        'user': request.user,
        'advertisements': advertisements
    })

def logout_view(request):
    logout(request)
    return redirect('app:home')


@login_required
def add_advertisement(request):

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, user=request.user)
        if form.is_valid():
            advertisement = form.save(commit=False)
            motor = form.cleaned_data['motor']
            # Assign user to motor if None
            if motor.user is None:
                motor.user = request.user
                motor.save()
            # Verify ownership
            elif motor.user != request.user:
                return HttpResponse("You can only advertise your own motors.", status=403)
            advertisement.user = request.user
            advertisement.save()
            return redirect('app:profile', user_id=request.user.id)
        else:
            return render(request, 'app/add_advertisement.html', {'form': form})
    else:
        form = AdvertisementForm(user=request.user)
        return render(request, 'app/add_advertisement.html', {'form': form})


@login_required
def add_motor(request):

    if request.method == 'POST':
        form = MotorForm(request.POST, request.FILES)
        if form.is_valid():
            motor = form.save(commit=False)
            motor.user = request.user
            motor.save()
            return redirect('app:add_advertisement')
        else:
            return render(request, 'app/add_motor.html', {'form': form})
    else:
        form = MotorForm()
        return render(request, 'app/add_motor.html', {'form': form})