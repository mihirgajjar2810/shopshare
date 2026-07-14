from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    query = request.GET.get('q')
    if query:
        products = products.filter( Q (name__icontains=query) | Q(description__icontains=query) )
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'products/product_details.html', {'product': product})