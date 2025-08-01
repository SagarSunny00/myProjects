from django.shortcuts import render

# Create your views here.
# Mangement/management/views.py
from .serializers import (
    ClientSerializer,
    ProjectSerializer,
    ProjectCreateSerializer,
    UserSerializerForProject
)
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Client, Project


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='projects')
    def create_project(self, request, pk=None):
        client = self.get_object()
        serializer = ProjectCreateSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            project = serializer.save(client=client, created_by=request.user)
            return Response(ProjectSerializer(project, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return Project.objects.filter(users=self.request.user).distinct()
        return Project.objects.all()

    def perform_create(self, serializer):
        pass

    def perform_update(self, serializer):
        serializer.save(updated_at=serializers.DateTimeField(
            read_only=True).to_representation(serializers.DateTimeField().now()))

    def perform_destroy(self, instance):
        instance.delete()
