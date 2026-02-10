from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart
import requests
from decimal import Decimal
import stripe
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty")
        return redirect('shop:product_list')

    tax_rate = Decimal('0.13')
    subtotal = cart.get_total_price()
    tax = subtotal * tax_rate
    grand_total = subtotal + tax

    # Create line items for Stripe
    line_items = []
    for item in cart:
        # Calculate unit price including tax for each item
        unit_price = Decimal(item['price'])
        # Add 13% tax to each unit price
        price_with_tax = unit_price * Decimal('1.13')
        
        line_items.append({
            'price_data': {
                'currency': 'npr',
                'product_data': {
                    'name': f"{item['product'].name} (Inc. 13% VAT)",
                },
                'unit_amount': int(price_with_tax.quantize(Decimal('1')) * 100),
            },
            'quantity': item['quantity'],
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('orders:order_history')) + '?status=success',
            cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"Error creating Stripe session: {str(e)}")
        return redirect('cart:cart_detail')

@login_required
def order_history(request):
    # CRITICAL: Clear cart and create order record upon successful return
    if request.GET.get('status') == 'success':
        cart = Cart(request)
        if len(cart) > 0:
            # Create the actual order in DB
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total_price(),
                is_paid=True
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            messages.success(request, "Payment successful! Your order has been placed.")
        
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_history.html', {'orders': orders})


def admin_check(user):
    return user.is_superuser



def send_receipt(order_id, email):
    order = Order.objects.get(id=order_id)
    subject = f'MeroKart Order #{order_id} - Tax Invoice'
    message = f'Dear Customer,\n\nYour order #{order_id} for Rs. {order.total_amount} has been successfully placed.\n'
    message += 'Thank you for shopping at MeroKart.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)