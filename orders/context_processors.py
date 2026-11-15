from .models import CartItem

def cart_context(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        total_qty = sum(item.quantity for item in items)
        total_price = sum(item.total_price for item in items)
        return {
            'cart_items_count': total_qty,
            'cart_total_price': total_price,
            'global_cart_items': items,
        }
    return {
        'cart_items_count': 0,
        'cart_total_price': 0,
        'global_cart_items': [],
    }
