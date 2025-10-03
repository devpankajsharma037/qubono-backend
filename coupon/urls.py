from django.urls import path,include
from .views import (StoreUserView,WishListView,CategoryView)


urlpatterns = [

    # Admin Routes
    path('admin/',include('coupon.admin_route')),

    # User Store View
    path('store/list/', StoreUserView.as_view({"get":"storeList"}),name='app-store-list'),
    path('store/<slug>', StoreUserView.as_view({"get":"storeBySlug"}),name='app-store-by-slug'),
    path('store/category/', StoreUserView.as_view({"get":"storeByCategory"}),name='app-store-by-category'),

    # User Store Coupon View
    path('store/coupon/', StoreUserView.as_view({"get":"storeCouponByFllter"}),name='app-store-coupon'),

    # User Wishlist View
    path('wishlist/', WishListView.as_view({"patch":"wishListCreateRemove"}),name='wishlist-create-remove'),
    path('wishlist/list/', WishListView.as_view({"get":"wishList"}),name='wishlist-list'),

    # User Category View
    path('category/', CategoryView.as_view({"get":"categoryListByFilter"}),name='category-list'),
]