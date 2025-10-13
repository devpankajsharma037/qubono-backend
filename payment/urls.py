from django.urls import path,include
from .views import *

urlpatterns = [
    path('order/', PaymentViewset.as_view({"post":"createOrder"}),name='create-order'),
    path('order/status/', PaymentViewset.as_view({"post":"paymentStatus"}),name='order-status'),
    path('order/list/', OrderViewset.as_view({"get":"userOrderList"}),name='order-list'),
    path('list/', PaymentViewset.as_view({"get":"paymentList"}),name='payment-list'),

    # Admin
    path('admin/payment/list/', PaymentViewset.as_view({"get":"adminPaymentList"}),name='payment-list'),
    path('admin/order/list/', OrderViewset.as_view({"get":"adminOrderList"}),name='order-list'),
]