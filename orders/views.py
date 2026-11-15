from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from products.models import Product
from .models import CartItem, Order, OrderItem
from accounts.models import User
import uuid

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.total_price for item in cart_items)
    shipping = 50.00 if subtotal > 0 else 0.00 # wholesale flat rate
    tax = subtotal * 0.05 # 5% VAT
    total = subtotal + shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 10)) # default 10kg wholesale minimum

    if qty > product.stock:
        messages.error(request, f"Cannot add {qty}kg. Only {product.stock}kg available in stock.")
        return redirect('products:detail', slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += qty
    else:
        cart_item.quantity = qty

    cart_item.save()
    messages.success(request, f"Added {qty}kg of {product.name} to your wholesale cart.")
    return redirect('orders:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"Removed {name} from your cart.")
    return redirect('orders:cart_detail')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        qty = int(request.POST.get('quantity', 1))
        if qty <= 0:
            cart_item.delete()
        else:
            if qty > cart_item.product.stock:
                messages.error(request, f"Cannot update to {qty}kg. Only {cart_item.product.stock}kg in stock.")
                return redirect('orders:cart_detail')
            cart_item.quantity = qty
            cart_item.save()
            messages.success(request, "Cart updated.")
    return redirect('orders:cart_detail')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('products:list')

    subtotal = sum(item.total_price for item in cart_items)
    shipping = 50.00
    tax = subtotal * 0.05
    total = subtotal + shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'wallet_balance': request.user.wallet_balance,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
@transaction.atomic
def process_checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('products:list')

        delivery_address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'Wallet')

        if not delivery_address:
            messages.error(request, "Delivery address is required.")
            return redirect('orders:checkout')

        subtotal = sum(item.total_price for item in cart_items)
        shipping = 50.00
        tax = subtotal * 0.05
        total = subtotal + shipping + tax

        # Check stock before processing
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Insufficient stock for {item.product.name}. Available: {item.product.stock}kg.")
                return redirect('orders:cart_detail')

        # Payment processing
        buyer = User.objects.select_for_update().get(id=request.user.id)
        if payment_method == 'Wallet':
            if buyer.wallet_balance < total:
                messages.error(request, f"Insufficient funds in wallet. Total required: ${total:,.2f}. Current balance: ${buyer.wallet_balance:,.2f}")
                return redirect('orders:checkout')
            
            buyer.wallet_balance -= total
            buyer.save()

        # Create Order
        order = Order.objects.create(
            buyer=buyer,
            status='PAID' if payment_method == 'Wallet' else 'PENDING',
            total_amount=total,
            payment_method=payment_method,
            delivery_address=delivery_address,
            tracking_number=f"TV-{uuid.uuid4().hex[:8].upper()}"
        )

        # Create Order Items and decrease stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart_items.delete()

        messages.success(request, f"Order #{order.id} placed successfully! Method: {payment_method}")
        return render(request, 'orders/success.html', {'order': order})

    return redirect('orders:checkout')
