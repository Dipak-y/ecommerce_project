from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_add, name="product_add"),
    path("products/edit/<int:pk>/", views.product_edit, name="product_edit"),
    path("products/delete/<int:pk>/", views.product_delete, name="product_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/edit/<int:pk>/", views.category_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", views.category_delete, name="category_delete"),
    path("variations/", views.variation_list, name="variation_list"),
    path("variations/add/", views.variation_add, name="variation_add"),
    path("variations/edit/<int:pk>/", views.variation_edit, name="variation_edit"),
    path("variations/delete/<int:pk>/", views.variation_delete, name="variation_delete"),
    path("orders/check/<int:pk>/", views.mark_order_checked, name="mark_order_checked"),
]
