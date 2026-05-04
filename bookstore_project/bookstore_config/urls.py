"""
URL configuration for bookstore_config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/orders/', RedirectView.as_view(pattern_name='admin_orders', permanent=True)),
    path('admin/orders/delete/<int:order_id>/', RedirectView.as_view(pattern_name='delete_order', permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('bookstore_app.urls')),
    path('api/', include('bookstore_app.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
