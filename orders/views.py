from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart
import requests
from decimal import Decimal
from django.shortcuts import redirect


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, is_checked_by_admin=False).order_by('-created')
    return render(request, 'orders/order_history.html', {'orders': orders})


def admin_check(user):
    return user.is_superuser



def send_receipt(order_id, email):
    order = Order.objects.get(id=order_id)
    subject = f'MeroKart Order #{order_id} - Tax Invoice'
    message = f'Dear Customer,\n\nYour order #{order_id} for Rs. {order.total_amount} has been successfully placed.\n'
    message += 'Thank you for shopping at MeroKart.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)