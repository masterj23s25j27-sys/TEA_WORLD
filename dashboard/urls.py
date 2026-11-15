from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('portal/buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('portal/vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('portal/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('portal/logistics/', views.delivery_portal, name='delivery_portal'),
]
