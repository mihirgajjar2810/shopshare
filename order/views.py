from django.shortcuts import render, redirect
from django.contrib import messages
from cart.utils import get_or_create_cart
from .models import Order, OrderItem
import random

def checkout(request):
    cart = get_or_create_cart(request)
    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('product_list')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        # Create Order
        order = Order.objects.create(
            first_name=first_name, last_name=last_name, email=email,
            address=address, city=city, postal_code=postal_code
        )
        if request.user.is_authenticated:
            order.user = request.user
            order.save()

        # Move CartItems to OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

            product = item.product
            if product.stock < item.quantity:
                messages.error(
                    request,
                    f"Only {product.stock} items available for {product.name}."
                )
                return redirect("view_cart")


            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart
        cart.items.all().delete()

        # Redirect to payment
        return redirect('process_order', order_id=order.id)

    return render(request, 'order/checkout.html', {'cart': cart})

def process_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        # Simulate payment success
        is_success = random.choice([True, True, True, False]) # 75% success rate
        
        if is_success:
            order.paid = True
            order.status = 'Paid'
            order.stripe_id = f"pi_mock_{random.randint(1000, 9999)}"
            order.save()
            messages.success(request, 'Payment successful! Your order is complete.')
            return redirect('home')
        else:
            messages.error(request, 'Payment failed. Please try again.')
            # Stays on the same page
            
    return render(request, 'order/payment.html', {'order': order})