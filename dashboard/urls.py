from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("products/", views.product_list, name="product_list"),
    path("categories/", views.category_list, name="category_list"),
    path("orders/", views.order_list, name="order_list"),
    path("users/", views.user_list, name="user_list"),
    path("profile/", views.admin_profile, name="admin_profile"),
]
