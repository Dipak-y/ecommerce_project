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


# -------------------------
# CART
# -------------------------

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.add(product=product, quantity=1)
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
    cart = Cart(request)

    if not len(cart):
        messages.error(request, "Your cart is empty")
        return redirect("cart:cart_detail")

    line_items = []
    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item["product"].name,
                },
                "unit_amount": int(Decimal(item["price"]) * 100),
            },
            "quantity": item["quantity"],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/cart/stripe/success/"),
        cancel_url=request.build_absolute_uri("/cart/stripe/cancel/"),
        customer_email=request.user.email,
    )

    return redirect(session.url, code=303)


@login_required
def stripe_success(request):
    cart = Cart(request)

    # Create Order
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.get_total_price(),
        is_paid=True,
    )

    # Create Order Items
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            price=item["price"],
            quantity=item["quantity"],
        )

    cart.clear()
    messages.success(request, "Payment successful! Order placed.")

    # ✅ Redirect to orders section
    return redirect("orders:order_history")


@login_required
def stripe_cancel(request):
    messages.warning(request, "Payment cancelled")
    return redirect("cart:cart_detail")
