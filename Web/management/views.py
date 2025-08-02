# management/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Client, Project
from .serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ProjectDetailSerializer, # For output of project creation/listing
    ProjectCreateSerializer  # For input of project creation
)

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed, created, updated or deleted.
    Supports nested project creation via a custom action.
    """
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated] # Requires authenticated users for all actions

    def get_serializer_class(self):
        """
        Returns different serializers based on the action.
        - `retrieve` action uses ClientDetailSerializer for nested projects.
        - Other actions (list, create, update) use ClientSerializer.
        """
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        """
        Save the client instance, automatically setting 'created_by' and 'updated_by'
        to the current authenticated user.
        """
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """
        Save the client instance, automatically setting 'updated_by'
        to the current authenticated user.
        """
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """
        Custom delete logic if needed (e.g., logging).
        """
        instance.delete()

    @action(detail=True, methods=['post'], url_path='projects')
    def create_project(self, request, pk=None):
        """
        Custom action to create a new project for a specific client.
        URL: POST /api/clients/{client_id}/projects/
        Input: {'project_name': 'Project A', 'users': [1, 2]}
        Output: Detailed project info.
        """
        # Get the client instance based on the URL's primary key (pk)
        client = get_object_or_404(Client, pk=pk)

        # Initialize the ProjectCreateSerializer with request data and context.
        # Pass 'client' and 'request' in context for serializer's create method.
        serializer = ProjectCreateSerializer(
            data=request.data,            context={'client': client, 'request': request}
        )

        if serializer.is_valid():
            # Save the project (this calls the custom create method in the serializer)
            project = serializer.save()
            # Return the detailed representation of the newly created project
            return Response(ProjectDetailSerializer(project, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows projects assigned to the logged-in user to be viewed.
    URL: GET /api/projects/
    """
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated] # Requires authenticated users

    def get_queryset(self):
        """
        Filters the projects to only show those assigned to the currently
        authenticated user.
        """
        # Ensure only projects where the requesting user is assigned are returned
        return Project.objects.filter(users=self.request.user).distinct().order_by('-created_at')