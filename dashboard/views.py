from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from shop.models import Product, Category

@staff_member_required
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-created')
    total_orders = orders.count()
    total_revenue = orders.filter(is_paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_customers = User.objects.filter(is_staff=False).count()
    
    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'orders': orders[:10],
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_products': products.count(),
        'total_categories': categories.count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})

@staff_member_required
def order_list(request):
    orders = Order.objects.all().order_by('-created')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_member_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@staff_member_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})

@staff_member_required
def admin_profile(request):
    return render(request, 'dashboard/admin_profile.html', {'admin_user': request.user})
