from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,get_object_or_404, redirect
from .forms import SignUpForm,LoginForm
from django.urls import reverse
from search_app.models import Product,CustomUser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search_app:search_view')  # ログイン後にリダイレクトするページ
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('search_app:search_view')  # ログイン後のリダイレクト先
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    #return redirect(reverse('search_app:search_view'))
    return redirect(reverse('account:login'))

def profile_view(request, username=None, user_id=None):
    if username:
        user = get_object_or_404(CustomUser, username=username)
    elif user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    product = Product.objects.all()
    
    context = {'user': user,'userproducts':product}
    return render(request, 'account/profile.html', context)