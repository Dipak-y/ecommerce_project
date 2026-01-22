from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from orders.models import Order

@staff_member_required
@staff_member_required
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-created')
    paid_orders = orders.filter(is_paid=True).count()
    pending_orders = orders.filter(is_paid=False).count()

    return render(request, 'dashboard/admin_dashboard.html', {
        'orders': orders,
        'paid_orders': paid_orders,
        'pending_orders': pending_orders,
    })

