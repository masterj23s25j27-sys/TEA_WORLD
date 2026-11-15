from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('tea/<slug:slug>/', views.product_detail, name='detail'),
    path('tea/<int:product_id>/add-review/', views.add_review, name='add_review'),
]
