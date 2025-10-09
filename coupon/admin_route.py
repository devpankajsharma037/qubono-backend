from django.urls import path
from .views import (
    StoreAdminView,
    CategoryAdminView,
    SubCategoryAdminView,
    UserAdminView
)

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

    # ===== SUBCATEGORY ROUTES =====
    path('store/category/subcategory/', SubCategoryAdminView.as_view({"get": "subCategoryList"}), name='subcategory-list'),
    path('store/category/subcategory/create/', SubCategoryAdminView.as_view({"post": "subCategoryCreate"}), name='subcategory-create'),
    path('store/category/subcategory/update/', SubCategoryAdminView.as_view({"patch": "subCategoryUpdate"}), name='subcategory-update'),
    path('store/category/subcategory/delete/<uuid:pk>/', SubCategoryAdminView.as_view({"delete": "subCategoryDelete"}), name='subcategory-delete'),

    # ===== USER ROUTES =====
    path('store/user/list/', UserAdminView.as_view({"get": "userListByFilter"}), name='user-list'),
    path('store/user/update/', UserAdminView.as_view({"patch": "updateUser"}), name='user-update'),
]
