from django.urls import path,include
from .views import (StoreUserView,WishList)


urlpatterns = [

    # Admin Routes
    path('admin/',include('admin_route')),
    

    # User Store View
    path('store/list/', StoreUserView.as_view({"get":"storeList"}),name='app-store-list'),
    path('store/<slug>', StoreUserView.as_view({"get":"storeBySlug"}),name='app-store-by-slug'),
    path('store/category/', StoreUserView.as_view({"get":"storeByCategory"}),name='app-store-by-category'),

    # User Store Coupon View
    path('store/coupon/', StoreUserView.as_view({"get":"storeCouponByFllter"}),name='app-store-coupon'),

    # User Wishlist View
    path('wishlist/', WishList.as_view({"patch":"wishListCreateRemove"}),name='wishlist-create-remove'),
    path('wishlist/list/', WishList.as_view({"get":"wishList"}),name='wishlist-list'),
]