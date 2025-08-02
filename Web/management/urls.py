# management/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
# For ProjectViewSet, we use basename because it's a ReadOnlyModelViewSet
# and doesn't have a default queryset attribute set, or if we want to override the default name.
router.register(r'projects', ProjectViewSet, basename='project')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]