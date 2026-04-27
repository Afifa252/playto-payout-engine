"""
URL configuration for playto_backend project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Added API routes
    path('api/v1/', include('payouts.urls')),
]