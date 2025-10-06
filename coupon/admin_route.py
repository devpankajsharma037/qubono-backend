from django.urls import path,include
from .views import (StoreAdminView,CategoryAdminView)


urlpatterns = [
    path('store/create/',   StoreAdminView.as_view({"post":"createStore"}),name='store-create'),
    path('store/list/',     StoreAdminView.as_view({"get":"storeList"}),name='store-list'),
    path('store/update/',   StoreAdminView.as_view({"patch":"updateStore"}),name='store-update'),
    path('store/<slug>',    StoreAdminView.as_view({"get":"storeBySlug","delete":"deleteStore"}),name='store-by-slug'),

    # Admin Store Coupon View
    path('store/coupon/',   StoreAdminView.as_view({"get":"storeCouponByFllter"}),name='store-coupon'),

    # Admin Category View
    path('store/category/',   CategoryAdminView.as_view({"get":"categoryListByFilter"}),name='store-category'),
]