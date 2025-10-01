from django.urls import path
from .views import (UserAuthView,ProfileView)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    # Auth View
    path('signup/', UserAuthView.as_view({"post":"register"}),name='signup'),
    path('activate-account/', UserAuthView.as_view({"post":"verfiyAccount"}),name='activate-account'),
    path('signin/', UserAuthView.as_view({"post":"login"}),name='signin'),
    path('forgot-password/', UserAuthView.as_view({"post":"forgotPassword"}),name='forgot-password'),
    path('reset-password/', UserAuthView.as_view({"post":"restPassword"}),name='reset-password'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    # Profile View
    path('profile/', ProfileView.as_view({"get":"getProfile"}),name='get-profile'),
    path('update-profile/', ProfileView.as_view({"patch":"updateProfile"}),name='update-profile'),
]