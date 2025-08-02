"""
URL configuration for Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Web/urls.py

from django.contrib import admin # <--- FIX APPLIED HERE: Import admin
from django.urls import path, include
from rest_framework.authtoken import views as authtoken_views # For obtaining authentication tokens

urlpatterns = [
    path('admin/', admin.site.urls), # Django Admin site
    path('api/', include('management.urls')), # Include URLs from our 'management' app
    path('api-token-auth/', authtoken_views.obtain_auth_token), # Endpoint to get auth token
]