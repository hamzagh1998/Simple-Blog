from blog.models import Post
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account Created For {}!'.format(username))
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form':form})

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def ProfileView(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    if request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account updated with successfully!')
            return redirect('home')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form':user_form, 'profile_form':profile_form, 'posts_list':Post.objects.all()})
