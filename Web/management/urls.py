# Mangement/management/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
# 'basename' is needed for non-queryset-based viewsets or when queryset is filtered
router.register(r'projects', ProjectViewSet, basename='project')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # Custom URL for creating projects under a client, handled by the @action decorator
    # The action automatically generates a URL like /clients/{pk}/projects/
    # No need to explicitly add it here if using @action on a ModelViewSet.
]
