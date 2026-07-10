from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import CartItem
from .utils import get_or_create_cart

def view_cart(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_details.html', {'cart': cart})

def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check stock
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} items left in stock.')
            return redirect(request.META.get('HTTP_REFERER', 'product_list'))

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        messages.success(request, f'Added {product.name} to cart.')
    return redirect('product_list')

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, f'Removed {item.product.name} from cart.')
    return redirect('view_cart')

def update_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            if item.quantity < item.product.stock:
                item.quantity += 1
                item.save()
                messages.success(request, f'Increased quantity for {item.product.name}.')
            else:
                messages.error(request, f'Cannot add more. Only {item.product.stock} in stock.')
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                messages.success(request, f'Decreased quantity for {item.product.name}.')
            else:
                item.delete()
                messages.info(request, f'Removed {item.product.name} from cart.')
    return redirect('view_cart')