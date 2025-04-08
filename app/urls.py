from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout')
]