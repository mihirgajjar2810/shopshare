from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from order.models import Order
from products.models import Product

# ---------------------------------------------------------- Read(R)_start ----------------------------------------------------------

@login_required(login_url='login')
def main_dashboard(request):
   
    if request.user.is_shopkeeper:
        return redirect('shopkeeper_dashboard')
    return redirect('customer_dashboard')

@login_required(login_url='login')
def customer_dashboard(request):
  
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/customer_dashboard.html', {'orders': orders})

@login_required(login_url='login')
def shopkeeper_dashboard(request):
  
    if not request.user.is_shopkeeper:
        return redirect('customer_dashboard')

    products = Product.objects.filter(shopkeeper=request.user)
    
    # Advanced logic: Find all orders that contain a product owned by this shopkeeper
    # We use double underscores `__` to query across relationships in Django.
    orders = Order.objects.filter(items__product__shopkeeper=request.user).distinct().order_by('-created_at')

    return render(request, 'dashboard/shopkeeper_dashbord.html', {
        'products': products,
        'orders': orders
    })
# ---------------------------------------------------------- Read(R)_End ----------------------------------------------------------

from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.contrib import messages
from products.forms import ProductForm
import uuid

# ---------------------------------------------------------- Create(C)_start ----------------------------------------------------------

@login_required(login_url='login')
def product_create(request):
    if not request.user.is_shopkeeper:
        return redirect('customer_dashboard')
        
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shopkeeper = request.user
            
            # Auto-generate slug
            base_slug = slugify(product.name)
            slug = base_slug
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            product.slug = slug
            
            product.save()
            messages.success(request, 'Product created successfully.')
            return redirect('shopkeeper_dashboard')
    else:
        form = ProductForm()
        
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})

# ---------------------------------------------------------- Create(C)_End ----------------------------------------------------------



# ---------------------------------------------------------- Update(U)_start ----------------------------------------------------------
@login_required(login_url='login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, shopkeeper=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # If name changed, we could update slug, but usually it's better to keep slug constant for SEO.
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('shopkeeper_dashboard')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product'})

# ---------------------------------------------------------- Update(U)_End ----------------------------------------------------------

# ---------------------------------------------------------- Delete(D)_start ----------------------------------------------------------
@login_required(login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, shopkeeper=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('shopkeeper_dashboard')
        
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

# ---------------------------------------------------------- Delete(D)_End ----------------------------------------------------------