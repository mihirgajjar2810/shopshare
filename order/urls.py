from django.urls import path
from . import views
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.process_payment, name='process_payment'),
]