from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from orders.models import Order
from shop.models import Product, Category, Variation
from .forms import ProductForm, CategoryForm, VariationForm

@staff_member_required
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-created')
    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'orders': orders,
        'products': products,
        'categories': categories,
        'paid_orders': orders.filter(is_paid=True).count(),
        'pending_orders': orders.filter(is_paid=False).count(),
        'total_revenue': sum(order.get_total_cost() if hasattr(order, 'get_total_cost') else order.total_amount for order in orders if order.is_paid),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required
def mark_order_checked(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.is_checked_by_admin = True
    order.save()
    messages.success(request, f"Order #{order.id} has been checked and removed from user view.")
    return redirect('dashboard:admin_dashboard')

@staff_member_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})

@staff_member_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})

@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product'})

@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('dashboard:product_list')

@staff_member_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@staff_member_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add Category'})

@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Edit Category'})

@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('dashboard:category_list')

@staff_member_required
def variation_list(request):
    product_id = request.GET.get('product')
    if product_id:
        variations = Variation.objects.filter(product_id=product_id)
        product = get_object_or_404(Product, id=product_id)
    else:
        variations = Variation.objects.all()
        product = None
    return render(request, 'dashboard/variation_list.html', {'variations': variations, 'product': product})

@staff_member_required
def variation_add(request):
    product_id = request.GET.get('product')
    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            variation = form.save()
            messages.success(request, 'Variation added successfully.')
            return redirect(f'/dashboard/variations/?product={variation.product.id}')
    else:
        initial = {}
        if product_id:
            initial['product'] = product_id
        form = VariationForm(initial=initial)
    return render(request, 'dashboard/variation_form.html', {'form': form, 'title': 'Add Variation'})

@staff_member_required
def variation_edit(request, pk):
    variation = get_object_or_404(Variation, pk=pk)
    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Variation updated successfully.')
            return redirect(f'/dashboard/variations/?product={variation.product.id}')
    else:
        form = VariationForm(instance=variation)
    return render(request, 'dashboard/variation_form.html', {'form': form, 'title': 'Edit Variation'})

@staff_member_required
def variation_delete(request, pk):
    variation = get_object_or_404(Variation, pk=pk)
    product_id = variation.product.id
    variation.delete()
    messages.success(request, 'Variation deleted successfully.')
    return redirect(f'/dashboard/variations/?product={product_id}')
