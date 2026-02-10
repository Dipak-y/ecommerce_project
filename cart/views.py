from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import stripe

from shop.models import Product
from .cart import Cart
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.views.decorators.http import require_POST


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')
    color = request.POST.get('color')

    cart.add(product=product, quantity=quantity, size=size, color=color)
    messages.success(request, f"{product.name} added to cart!")
    return redirect("cart:cart_detail")


def cart_update_quantity(request, key, action):
    cart = Cart(request)

    if key not in cart.cart:
        messages.error(request, "Item not found in cart")
        return redirect("cart:cart_detail")

    if action == "increase":
        cart.cart[key]["quantity"] += 1
    elif action == "decrease":
        cart.cart[key]["quantity"] -= 1

    if cart.cart[key]["quantity"] <= 0:
        cart.remove(key)
    else:
        cart.save()

    return redirect("cart:cart_detail")


def cart_remove(request, key):
    Cart(request).remove(key)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    subtotal = cart.get_total_price()
    tax = subtotal * Decimal("0.13")
    grand_total = subtotal + tax

    return render(request, "cart/detail.html", {
        "cart": cart,
        "tax": tax,
        "grand_total": grand_total,
    })


# -------------------------
# STRIPE CHECKOUT
# -------------------------


@login_required
def checkout(request):
    """
    Simplified checkout that redirects to the centralized orders:create_checkout_session.
    """
    return redirect('orders:create_checkout_session')

@login_required
def stripe_success(request):
    """
    Handled in orders:order_history now, but kept as a fallback.
    """
    return redirect("orders:order_history")

@login_required
def stripe_cancel(request):
    messages.warning(request, "Payment cancelled")
    return redirect("cart:cart_detail")
