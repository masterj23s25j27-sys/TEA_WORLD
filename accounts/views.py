from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from .models import User
from decimal import Decimal

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'BUYER')
        company_name = request.POST.get('company_name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        if not username or not password or not email:
            messages.error(request, "Username, email, and password are required.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            company_name=company_name,
            phone=phone,
            address=address
        )
        login(request, user)
        messages.success(request, f"Welcome to sha_Tea, {user.username}!")
        return redirect('dashboard:home')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('dashboard:home')

@transaction.atomic
def recharge_wallet(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        amount = request.POST.get('amount', '0')
        try:
            val = Decimal(amount)
            if val > 0:
                user = User.objects.select_for_update().get(id=request.user.id)
                user.wallet_balance += val
                user.save()
                messages.success(request, f"Deposited ${val:,.2f} into your digital wallet.")
            else:
                messages.error(request, "Invalid recharge amount.")
        except Exception:
            messages.error(request, "Error processing payment transaction.")
    return redirect('dashboard:buyer_dashboard')
