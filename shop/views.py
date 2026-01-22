from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Product, Category, Variation



def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def profile(request):
    return render(request, 'shop/profile.html')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('search')
    if query:
        products = products.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    if request.path == '/':
        return render(request, 'shop/index.html', {'products': products})

    return render(request, 'shop/list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)

    # Fetch variations
    colors = Variation.objects.colors().filter(product=product)
    sizes = Variation.objects.sizes().filter(product=product)

    context = {
        'product': product,
        'colors': colors,
        'sizes': sizes,
    }

    return render(request, 'shop/detail.html', context)

