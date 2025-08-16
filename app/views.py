from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout, login as auth_login, authenticate
from .forms import AuthenticationForm, UserForm, AccountForm, AdvertisementForm, MotorForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Motor, Advertisement
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now

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
            if motor.user is None:
                motor.user = request.user
                motor.save()
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
        print("POST request, form is valid:", form.is_valid())
        if form.is_valid():
            motor = form.save(commit=False)
            motor.user = request.user
            motor.save()
            return redirect('app:add_advertisement')
        else:
            print("Form errors:", form.errors)
            return render(request, 'app/add_motor.html', {'form': form})
    else:
        form = MotorForm()
        print("GET request, rendering form")
        return render(request, 'app/add_motor.html', {'form': form})
    

def all_advertisements(request):
    ads = Advertisement.objects.filter(is_active=True)

    query = request.GET.get('q', '')
    if query:
        terms = query.lower().split()
        condition_keywords = ['new', 'excellent', 'very', 'good', 'not', 'working', 'smaller', 'investments', 'required']

        condition_filters = Q()
        for term in terms:
            if term.isdigit():
                if len(term) == 4:  
                    ads = ads.filter(motor__made_at=term)
                else:  
                    ads = ads.filter(
                        Q(motor__mileage__lte=term) |
                        Q(motor__price__lte=term) |
                        Q(motor__power__lte=term)
                    )
            elif term in condition_keywords:
                condition_filters |= Q(motor__condition__icontains=term)
            else:
                ads = ads.filter(
                    Q(motor__brand__icontains=term) |
                    Q(motor__model__icontains=term) |
                    Q(motor__name__icontains=term) |
                    Q(motor__description__icontains=term) |
                    Q(motor__condition__icontains=term) |
                    Q(user__location__icontains=term)
                )
        if condition_filters:
            ads = ads.filter(condition_filters)

    brand = request.GET.get('brand')
    model = request.GET.get('model')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    min_mileage = request.GET.get('min_mileage')
    max_mileage = request.GET.get('max_mileage')
    condition = request.GET.get('condition')
    min_power = request.GET.get('min_power')
    max_power = request.GET.get('max_power')
    location = request.GET.get('location')

    if brand:
        ads = ads.filter(motor__brand__icontains=brand)
    if model:
        ads = ads.filter(motor__model__icontains=model)
    if min_price:
        ads = ads.filter(motor__price__gte=min_price)
    if max_price:
        ads = ads.filter(motor__price__lte=max_price)
    if min_year:
        ads = ads.filter(motor__made_at__gte=min_year)
    if max_year:
        ads = ads.filter(motor__made_at__lte=max_year)
    if min_mileage:
        ads = ads.filter(motor__mileage__gte=min_mileage)
    if max_mileage:
        ads = ads.filter(motor__mileage__lte=max_mileage)
    if condition:
        ads = ads.filter(motor__condition=condition)
    if min_power:
        ads = ads.filter(motor__power__gte=min_power)
    if max_power:
        ads = ads.filter(motor__power__lte=max_power)
    if location:
        ads = ads.filter(user__location__icontains=location)

    favorites = []
    if request.user.is_authenticated:
        favorites = request.user.favorite_ads.values_list('id', flat=True)

    brands = Motor.objects.values_list('brand', flat=True).distinct()
    models = Motor.objects.values_list('model', flat=True).distinct()
    locations = CustomUser.objects.values_list('location', flat=True).distinct()

    return render(request, 'app/all_ads.html', {
        'ads': ads,
        'favorites': favorites,
        'brands': brands,
        'models': models,
        'locations': locations,
        'request' : request,
        'now' : now(),
    })


@login_required
def toggle_favorite(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)

    if ad.user == request.user:
        messages.warning(request, "You cannot add your own ad to favorites.")
        return redirect('app:ad_detail', ad_id=ad_id)

    if ad in request.user.favorite_ads.all():
        request.user.favorite_ads.remove(ad)
        messages.success(request, "Ad removed from your favorites.")
    else:
        request.user.favorite_ads.add(ad)
        messages.success(request, "Ad added to your favorites.")

    return redirect('app:ad_detail', ad_id=ad_id)


@login_required
def favorite_ads_view(request):
    favorites = Advertisement.objects.filter(favorited_by=request.user)
    return render(request, 'app/favorites.html', {'favorites': favorites})


@login_required
def ad_detail(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    motor = ad.motor  

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = ad in request.user.favorite_ads.all()

    return render(request, 'app/ad_detail.html', {
        'ad': ad,
        'motor': motor,
        'is_favorite': is_favorite
    })

@login_required
def edit_motor(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id, user=request.user)

    if request.method == 'POST':
        form = MotorForm(request.POST, request.FILES, instance=motor)
        if form.is_valid():
            form.save()
            return redirect('app:profile', user_id=request.user.id)  
    else:
        form = MotorForm(instance=motor)

    return render(request, 'app/edit_motor.html', {'form': form, 'motor': motor})


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id, user=request.user)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('app:profile', user_id=request.user.id)
    else:
        form = AdvertisementForm(instance=ad)

    return render(request, 'app/edit_ad.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id, user=request.user)

    if request.method == 'POST':
        ad.delete()
        return redirect('app:profile', user_id=request.user.id)

    return render(request, 'app/confirm_delete.html', {'ad': ad})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('app:profile', user_id=request.user.id)  
    else:
        form = AccountForm(instance=request.user)
    return render(request, 'app/edit_profile.html', {'form': form})

class MyPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'app/password_change.html'
    success_url = reverse_lazy('app:password_change_done')

class MyPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'app/password_change_done.html'

@login_required
def quiz_view(request):
    return render(request, 'app/quiz.html')

@login_required
def quiz_results(request):
    if request.method == 'POST':
        driving_style = request.POST.get('driving_style')
        budget = request.POST.get('budget')
        age_pref = request.POST.get('age_pref')
        mileage_pref = request.POST.get('mileage_pref')
        brand = request.POST.get('brand')

        ads = Advertisement.objects.filter(is_active=True)

        current_year = timezone.now().year
        recommended_ads = []

        for ad in ads:
            motor = ad.motor
            score = 0

            if driving_style == 'beginner':
                if motor.condition in ['new', 'excellent'] and motor.price <= 5000:
                    score += 1
            elif driving_style == 'adventurer':
                if motor.condition in ['good','very good', 'smaller investments required']:
                    score += 1
            elif driving_style == 'experienced':
                if 5000 <= motor.price <= 15000:
                    score += 1

            if budget == 'low' and motor.price <= 5000:
                score += 1
            elif budget == 'mid' and 5000 <= motor.price <= 10000:
                score += 1
            elif budget == 'high' and motor.price >= 10000:
                score += 1

            motor_age = current_year - motor.made_at
            if age_pref == 'new' and motor.made_at >= current_year - 3:
                score += 1
            elif age_pref == 'old' and motor.made_at < current_year - 8:
                score += 1
            elif age_pref == 'any':
                score += 1

            if mileage_pref == 'low' and motor.mileage <= 10000:
                score += 1
            elif mileage_pref == 'medium' and motor.mileage <= 30000:
                score += 1
            elif mileage_pref == 'any':
                score += 1

            if brand == 'any' or motor.brand.lower() == brand.lower():
                score += 1

            if score >= 4:
                recommended_ads.append(ad)

        return render(request, 'app/quiz_results.html', {'recommended_motors': recommended_ads})
    else:
        return redirect('quiz')
