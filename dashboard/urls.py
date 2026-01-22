from django.urls import path
from dashboard.views import admin_dashboard

app_name = "dashboard"

urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
]
