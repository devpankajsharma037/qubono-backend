from django.urls import path
from .views import (
    StoreAdminView,
    CategoryAdminView,
    SubCategoryAdminView,
    UserAdminView,
    NotificationView
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
    path('store/category/subcategory/list', SubCategoryAdminView.as_view({"get": "subCategoryListByFilter"}), name='subcategory-list'),
    path('store/category/subcategory/create/', SubCategoryAdminView.as_view({"post": "subCategoryCreate"}), name='subcategory-create'),
    path('store/category/subcategory/update/', SubCategoryAdminView.as_view({"patch": "subCategoryUpdate"}), name='subcategory-update'),
    path('store/category/subcategory/delete/<uuid:uuid>/', SubCategoryAdminView.as_view({"delete": "subCategoryDelete"}), name='subcategory-delete'),

    # ===== USER ROUTES =====
    path('store/user/list/', UserAdminView.as_view({"get": "userListByFilter"}), name='user-list'),
    path('store/user/update/', UserAdminView.as_view({"patch": "updateUser"}), name='user-update'),

    # ===== NOTIFICATION =====
    path('store/notification/list/', NotificationView.as_view({"get": "notificationList"}), name='notification-list'),
    path('store/notification/create/', NotificationView.as_view({"post": "notificationCreate"}), name='notification-create'),
    path('store/notification/update/', NotificationView.as_view({"patch": "notificationUpdate"}), name='notification-update'),
    path('store/notification/read/<uuid:pk>/', NotificationView.as_view({"patch": "notificationMarkRead"}), name='notification-seen'),
    path('store/notification/delete/<uuid:pk>/', NotificationView.as_view({"delete": "notificationDelete"}), name='notification-delete'),
]
