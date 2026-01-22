from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("remove/<str:key>/", views.cart_remove, name="cart_remove"),
    path(
        "update/<str:key>/<str:action>/",
        views.cart_update_quantity,
        name="cart_update_quantity",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("stripe/success/", views.stripe_success, name="stripe_success"),
    path("stripe/cancel/", views.stripe_cancel, name="stripe_cancel"),
]
