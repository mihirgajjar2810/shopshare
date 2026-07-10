from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_dashboard, name='dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('shopkeeper/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),
    path('shopkeeper/product/add/', views.product_create, name='product_create'),
    path('shopkeeper/product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('shopkeeper/product/delete/<int:pk>/', views.product_delete, name='product_delete'),
]