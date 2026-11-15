from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.db.models import Sum

def home(request):
    featured_products = Product.objects.all()[:4]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def buyer_dashboard(request):
    if request.user.role != 'BUYER' and not request.user.is_superuser:
        messages.warning(request, "Access restricted to Buyer Accounts.")
        return redirect('dashboard:home')

    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    # Calculate lifetime savings / bulk order count
    total_spent = orders.filter(status='DELIVERED').aggregate(total=Sum('total_amount'))['total'] or 0
    orders_count = orders.count()

    context = {
        'orders': orders,
        'total_spent': total_spent,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/buyer.html', context)

@login_required
def vendor_dashboard(request):
    if request.user.role != 'VENDOR' and not request.user.is_superuser:
        messages.warning(request, "Access restricted to Vendor Accounts.")
        return redirect('dashboard:home')

    # Get products owned by vendor
    my_products = Product.objects.filter(vendor=request.user)
    
    # Calculate stats
    total_sales = OrderItem.objects.filter(product__vendor=request.user, order__status='DELIVERED').aggregate(total=Sum('price'))['total'] or 0
    active_orders = Order.objects.filter(items__product__vendor=request.user).exclude(status__in=['DELIVERED', 'CANCELLED']).distinct()
    
    # Add new product form processing
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        origin = request.POST.get('origin', 'Assam, India')
        grade = request.POST.get('grade', 'OP')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description', '')
        
        category = get_object_or_404(Category, id=category_id)
        
        Product.objects.create(
            name=name,
            category=category,
            origin=origin,
            grade=grade,
            price=price,
            stock=stock,
            description=description,
            vendor=request.user,
            image_url='https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=600&auto=format&fit=crop&q=60'
        )
        messages.success(request, f"New tea variety '{name}' listed successfully!")
        return redirect('dashboard:vendor_dashboard')

    categories = Category.objects.all()
    context = {
        'products': my_products,
        'total_sales': total_sales,
        'active_orders': active_orders,
        'categories': categories,
        'grades': Product.GRADE_CHOICES,
    }
    return render(request, 'dashboard/vendor.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_platform_admin():
        messages.warning(request, "Unauthorized. Staff credentials required.")
        return redirect('dashboard:home')

    users = User.objects.all().order_by('-date_joined')
    products = Product.objects.all()
    orders = Order.objects.all().order_by('-created_at')
    
    total_revenue = Order.objects.filter(status='DELIVERED').aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = Order.objects.count()
    low_stock = Product.objects.filter(stock__lt=100).count()

    context = {
        'users': users,
        'products': products,
        'orders': orders,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'low_stock': low_stock,
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
def delivery_portal(request):
    # Available to delivery agents or distributors
    if request.user.role not in ['DELIVERY', 'DISTRIBUTOR'] and not request.user.is_superuser:
        messages.warning(request, "Access restricted to Delivery & Distributor Partners.")
        return redirect('dashboard:home')

    orders = Order.objects.all().order_by('-created_at')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        return redirect('dashboard:delivery_portal')

    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/delivery.html', context)
