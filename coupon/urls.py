from django.urls import path,include
from .views import (StoreUserView,WishListLoggedView,CategoryView,RatingView,RatingLoggedView)


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
    path('wishlist/', WishListLoggedView.as_view({"patch":"wishListCreateRemove"}),name='wishlist-create-remove'),
    path('wishlist/list/', WishListLoggedView.as_view({"get":"wishList"}),name='wishlist-list'),

    # User Category View
    path('category/', CategoryView.as_view({"get":"categoryListByFilter"}),name='category-list'),

    # User Category View
    path('store/rating/list/', RatingView.as_view({"get":"ratingListView"}),name='rating-list'),
    path('store/rating/create/', RatingLoggedView.as_view({"post":"ratingCreate"}),name='rating-create'),

]