from django.urls import path
from .views import (StoreAdminView,CategoryAdminView,UserAdminView,SubCategoryAdminView)


urlpatterns = [
    # Store View
    path('store/create/',   StoreAdminView.as_view({"post":"createStore"}),name='store-create'),
    path('store/list/',     StoreAdminView.as_view({"get":"storeList"}),name='store-list'),
    path('store/update/',   StoreAdminView.as_view({"patch":"updateStore"}),name='store-update'),
    path('store/<slug>',    StoreAdminView.as_view({"get":"storeBySlug","delete":"deleteStore"}),name='store-by-slug'),

    # Coupon View
    path('store/coupon/',   StoreAdminView.as_view({"get":"storeCouponByFllter"}),name='store-coupon'),
    path('store/coupon/create/',   StoreAdminView.as_view({"post":"storeCouponCreate"}),name='store-coupon-create'),
    path('store/coupon/update/',   StoreAdminView.as_view({"patch":"storeCouponUpdate"}),name='store-coupon-update'),
    path('store/coupon/delete/',   StoreAdminView.as_view({"delete":"storeCouponDelete"}),name='store-coupon-delete'),

    # Gift Card View
    path('store/card/',   StoreAdminView.as_view({"get":"storeGiftCardByFllter"}),name='store-coupon'),
    path('store/card/create/',   StoreAdminView.as_view({"post":"storeGiftCardCreate"}),name='store-card-create'),
    path('store/card/update/',   StoreAdminView.as_view({"patch":"storeGiftCardUpdate"}),name='store-card-update'),
    path('store/card/delete/',   StoreAdminView.as_view({"delete":"storeGiftCardDelete"}),name='store-card-delete'),


    # Provider View
    path('store/card/provider/',   StoreAdminView.as_view({"get":"providerByFllter"}),name='provider-list'),
    path('store/card/provider/create/',   StoreAdminView.as_view({"post":"providerCreate"}),name='provider-create'),
    path('store/card/provider/update/',   StoreAdminView.as_view({"patch":"providerUpdate"}),name='provider-update'),
    path('store/card/provider/delete/',   StoreAdminView.as_view({"delete":"providerDelete"}),name='provider-delete'),

    # Category View
    path('store/category/list/',   CategoryAdminView.as_view({"get":"categoryListByFilter"}),name='store-category'),
    path('store/category/<uuid>/',   CategoryAdminView.as_view({"get":"singleCategory"}),name='store-category-single'),
    path('store/category/create/',   CategoryAdminView.as_view({"post":"categoryCreate"}),name='store-category-create'),
    path('store/category/update/',   CategoryAdminView.as_view({"patch":"categoryUpdate"}),name='store-category-update'),
    path('store/category/delete/<uuid>/',   CategoryAdminView.as_view({"delete":"categoryDelete"}),name='store-category-delete'),

    # Category View
    path('store/category/subcategory/create/',   SubCategoryAdminView.as_view({"post":"subCategoryCreate"}),name='store-subcategory-create'),
    path('store/category/subcategory/update/',   SubCategoryAdminView.as_view({"patch":"subCategoryUpdate"}),name='store-subcategory-update'),
    path('store/category/subcategory/<uuid>/',   SubCategoryAdminView.as_view({"get":"singleSubCategory"}),name='store-subcategory-get'),
    path('store/category/subcategory/delete/<uuid>/',   SubCategoryAdminView.as_view({"delete":"subCategoryDelete"}),name='store-subcategory-delete'),
    
    # User View
    path('store/user/list/',   UserAdminView.as_view({"get":"userListByFilter"}),name='store-user'),
    path('store/user/update/',   UserAdminView.as_view({"patch":"updateUser"}),name='store-user-update'),
]