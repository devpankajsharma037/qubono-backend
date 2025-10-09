from django.urls import path,include
from .views import (StoreAdminView,CategoryAdminView,UserAdminView)



urlpatterns = [
    # ===== STORE ROUTES =====
    path('store/create/', StoreAdminView.as_view({"post": "createStore"}), name='store-create'),
    path('store/list/', StoreAdminView.as_view({"get": "storeList"}), name='store-list'),
    path('store/update/', StoreAdminView.as_view({"patch": "updateStore"}), name='store-update'),
    path('store/<slug:slug>/', StoreAdminView.as_view({"get": "storeBySlug", "delete": "deleteStore"}), name='store-detail'),

    # ===== COUPON ROUTE =====
    path('store/coupon/', StoreAdminView.as_view({"get": "storeCouponByFllter"}), name='store-coupon'),

    # ===== CATEGORY ROUTES =====
    path('store/category/list/', CategoryAdminView.as_view({"get": "categoryListByFilter"}), name='category-list'),
    path('store/category/<uuid:uuid>/', CategoryAdminView.as_view({"get": "singleCategory"}), name='category-detail'),
    path('store/category/create/', CategoryAdminView.as_view({"post": "categoryCreate"}), name='category-create'),
    path('store/category/update/', CategoryAdminView.as_view({"patch": "categoryUpdate"}), name='category-update'),
    path('store/category/delete/<uuid:uuid>/', CategoryAdminView.as_view({"delete": "categoryDelete"}), name='category-delete'),

    # User View
    path('store/user/list/',   UserAdminView.as_view({"get":"userListByFilter"}),name='store-user'),
    path('store/user/update/',   UserAdminView.as_view({"patch":"updateUser"}),name='store-user-update'),
]
