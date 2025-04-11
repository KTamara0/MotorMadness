from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_advertisement, name='add_advertisement'), 
    path('add-motor/', views.add_motor, name='add_motor'),
]