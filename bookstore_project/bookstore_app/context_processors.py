"""Context processors for bookstore app"""
from bookstore_app.models import Cart

def cart_context(request):
    """Add cart information to all templates"""
    cart_items = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.get_total_items()
            cart_total = cart.get_total_price_vnd()
        except Cart.DoesNotExist:
            pass
    
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
