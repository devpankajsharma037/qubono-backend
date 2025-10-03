from django.urls import path
from .views import (StoreAdminView,StoreUserView,UserStoreWishList)


urlpatterns = [

    # Admin Store View
    path('admin/store/create/', StoreAdminView.as_view({"post":"createStore"}),name='store-create'),
    path('admin/store/list/', StoreAdminView.as_view({"get":"storeList"}),name='store-list'),
    path('admin/store/update/', StoreAdminView.as_view({"patch":"updateStore"}),name='store-update'),
    path('admin/store/<slug>', StoreAdminView.as_view({"get":"storeBySlug","delete":"deleteStore"}),name='store-by-slug'),

    # User Store View
    path('store/list/', StoreUserView.as_view({"get":"storeList"}),name='app-store-list'),
    path('store/<slug>', StoreUserView.as_view({"get":"storeBySlug"}),name='app-store-by-slug'),

    # User Store Wishlist View
    path('wishlist/', UserStoreWishList.as_view({"get":"wishList"}),name='wish-list'),
]