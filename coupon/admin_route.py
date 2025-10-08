from django.urls import path,include
from .views import (StoreAdminView,CategoryAdminView)


urlpatterns = [
    # Store View
    path('store/create/',   StoreAdminView.as_view({"post":"createStore"}),name='store-create'),
    path('store/list/',     StoreAdminView.as_view({"get":"storeList"}),name='store-list'),
    path('store/update/',   StoreAdminView.as_view({"patch":"updateStore"}),name='store-update'),
    path('store/<slug>',    StoreAdminView.as_view({"get":"storeBySlug","delete":"deleteStore"}),name='store-by-slug'),

    # Coupon View
    path('store/coupon/',   StoreAdminView.as_view({"get":"storeCouponByFllter"}),name='store-coupon'),

    # Category View
    path('store/category/',   CategoryAdminView.as_view({"get":"categoryListByFilter"}),name='store-category'),
    path('store/category/create/',   CategoryAdminView.as_view({"post":"categoryCreate"}),name='store-category-create'),
    path('store/category/update/<uuid:pk>/',   CategoryAdminView.as_view({"patch":"categoryUpdate"}),name='store-category-update'),
    path('store/category/delete/<uuid:pk>/',   CategoryAdminView.as_view({"delete":"categoryDelete"}),name='store-category-delete'),
]