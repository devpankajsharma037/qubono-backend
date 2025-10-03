from django.urls import path
from .views import (StoreAdminView,StoreUserView)


urlpatterns = [

    # Admin Store View
    path('store/create/', StoreAdminView.as_view({"post":"createStore"}),name='store-create'),
    path('store/list/', StoreAdminView.as_view({"get":"storeList"}),name='store-list'),
    path('store/update/', StoreAdminView.as_view({"patch":"updateStore"}),name='store-update'),
    path('store/<slug>', StoreAdminView.as_view({"get":"storeBySlug","delete":"deleteStore"}),name='store-by-slug'),

    # User Store View
    path('app/store/list/', StoreUserView.as_view({"get":"storeList"}),name='app-store-list'),
    path('app/store/<slug>', StoreUserView.as_view({"get":"storeBySlug"}),name='app-store-by-slug'),
]