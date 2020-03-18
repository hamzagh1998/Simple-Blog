from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.log_in, name='login'),
    path('profile/', views.ProfileView, name='profile'),
]
