from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import MyPasswordChangeView, MyPasswordChangeDoneView

app_name = "app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_advertisement, name='add_advertisement'), 
    path('add-motor/', views.add_motor, name='add_motor'),
    path('ads/', views.all_advertisements, name='all_ads'),
    path('ads/favorite/<int:ad_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_ads_view, name='favorites'),
    path('my-ads/', views.my_ads, name='my_ads'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ads/edit/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('ads/delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', MyPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('quiz/results/', views.quiz_results, name='quiz_results'),
]