"""
URL configuration for b2broker_api project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('wallets.urls')),
]
