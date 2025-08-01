from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Client, Project
from django.utils import timezone

User = get_user_model()

# --- Client Serializers ---


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source='created_by.username', read_only=True)
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects',
                  'created_at', 'created_by', 'updated_at']

    def get_projects(self, obj):
        return [{'id': project.id, 'name': project.name} for project in obj.projects.all()]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.client_name = validated_data.get(
            'client_name', instance.client_name)
        # Fix: Use timezone.now() to get the current time
        instance.updated_at = timezone.now()
        instance.save()
        return instance

# --- Project Serializers ---


class UserSerializerForProject(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    client = serializers.CharField(source='client.client_name', read_only=True)
    users = UserSerializerForProject(many=True, read_only=True)
    created_by = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client',
                  'users', 'created_at', 'created_by']


class ProjectCreateSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    users = UserSerializerForProject(many=True, required=False)
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client',
                  'users', 'created_at', 'created_by']

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        project = Project.objects.create(**validated_data)
        for user_data in users_data:
            user_id = user_data.get('id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    project.users.add(user)
                except User.DoesNotExist:
                    print(
                        f"Warning: User with ID {user_id} not found for project {project.name}")
        return project

    def update(self, instance, validated_data):
        users_data = validated_data.pop('users', None)
        instance.name = validated_data.get('name', instance.name)
        instance.client = validated_data.get('client', instance.client)
        # instance.updated_at = timezone.now() # Uncomment if Project model has updated_at

        instance.save()

        if users_data is not None:
            instance.users.clear()
            for user_data in users_data:
                user_id = user_data.get('id')
                if user_id:
                    try:
                        user = User.objects.get(id=user_id)
                        instance.users.add(user)
                    except User.DoesNotExist:
                        print(
                            f"Warning: User with ID {user_id} not found during project update.")

        return instance
