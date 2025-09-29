from django.contrib import admin
from django.urls import path,include

admin.site.site_header = "Qubono"
admin.site.site_title = "Qubono"
admin.site.index_title = "Qubono"


urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/', include('customer.urls')),
]
