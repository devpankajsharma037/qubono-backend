from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Qubono"
admin.site.site_title = "Qubono"
admin.site.index_title = "Qubono"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('customer.urls')),
    path('api/v1/coupon/', include('coupon.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)