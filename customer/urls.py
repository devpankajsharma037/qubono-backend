from django.urls import path
from .views import (UserRegistrationView)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('v1/signup/', UserRegistrationView.as_view({"post":"post"}),name='signup'),
    path('v1/refresh/', TokenRefreshView.as_view(), name='refresh'),
]