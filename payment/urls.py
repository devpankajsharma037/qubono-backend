from django.urls import path,include
from .views import *

urlpatterns = [
    path('order/', PaymentViewset.as_view({"post":"createOrder"}),name='create-order'),
    path('order/status/', PaymentViewset.as_view({"post":"paymentStatus"}),name='order-status'),
]