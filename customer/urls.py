from django.urls import path
from .views import (UserAuthView)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('v1/signup/', UserAuthView.as_view({"post":"register"}),name='signup'),
    path('v1/signin/', UserAuthView.as_view({"post":"login"}),name='signin'),
    path('v1/refresh/', TokenRefreshView.as_view(), name='refresh'),
]