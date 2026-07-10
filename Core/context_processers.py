from products.models import Category
from cart.utils import get_or_create_cart

def global_data(request):
    categories = Category.objects.all()

    cart_count = 0
    if request.user.is_authenticated:
        if hasattr(request.user, 'cart'):
            cart_count = sum(item.quantity for item in request.user.cart.items.all())

        else:
            session_key = request.session.session_key
            if session_key:
                from cart.models import Cart
                cart = Cart.objects.filter(session_key=session_key).first()
                if cart:
                    cart_count = sum(item.quantity for item in cart.items.all())

                
    return {
            'global_categories': categories,
            'cart_count': cart_count,
            }
        