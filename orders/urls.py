from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("history/", views.order_history, name="order_history"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
]
