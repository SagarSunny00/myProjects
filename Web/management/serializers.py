# management/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, showing only id and username (as 'name').
    Used for nested representation within other serializers.
    """
    name = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name']

class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing projects within a client's detail view (GET /clients/:id/).
    Shows only id and project_name.
    """
    project_name = serializers.CharField(source='name', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name']

class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Project, used for retrieving a single project
    or for the output of project creation.
    Includes client name, assigned users, and creator/updater info.
    """
    project_name = serializers.CharField(source='name', help_text="The name of the project.")
    client = serializers.CharField(source='client.client_name', read_only=True, help_text="The name of the client this project belongs to.")
    users = UserSerializer(many=True, read_only=True, help_text="List of users assigned to this project.")
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    updated_by = serializers.CharField(source='updated_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['id', 'client', 'users', 'created_at', 'created_by', 'updated_at', 'updated_by']

class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new project.
    Accepts 'project_name' and a list of 'user_ids' for assignment.
    Handles the creation logic in its create method.
    """
    project_name = serializers.CharField(source='name', help_text="The name of the project to create.")
    # Custom field to accept a list of user IDs for assignment
    users = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        write_only=True,  # This field is only for input, not output
        required=False,
        allow_empty=True,
        help_text="A list of user IDs to assign to this project. Users must exist."
    )

    class Meta:
        model = Project
        fields = ['project_name', 'users']  # Fields accepted for input

    def create(self, validated_data):
        """
        Custom create method to handle user assignment and context-based client.
        """
        user_ids = validated_data.pop('users', [])
        project_name = validated_data.pop('name')  # Get the actual model field name 'name'

        # Retrieve client from serializer context, passed from the view
        client = self.context.get('client')
        if not client:
            raise serializers.ValidationError("Client must be provided in the context for project creation.")
        
        request = self.context.get('request')
        current_user = request.user if request else None

        # Create the project instance
        project = Project.objects.create(
            name=project_name,
            client=client,
            created_by=current_user,
            updated_by=current_user
        )

        # Assign users to the project
        if user_ids:
            # Filter for valid users to prevent errors from non-existent IDs
            valid_users = User.objects.filter(id__in=user_ids)
            if len(valid_users) != len(user_ids):
                # Optionally, you could raise a warning or specific error for invalid IDs
                pass
            project.users.set(valid_users)  # Assigns users using set() for ManyToMany

        return project

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for Client model, used for listing, creating, and updating clients.
    Includes read-only fields for created_by and updated_by.
    """
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    updated_by = serializers.CharField(source='updated_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['id', 'created_at', 'created_by', 'updated_at', 'updated_by']  # These fields are system-managed

    def create(self, validated_data):
        """
        Automatically sets created_by and updated_by on client creation.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Automatically sets updated_by on client update.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)

class ClientDetailSerializer(ClientSerializer):
    """
    Extended ClientSerializer for detailed view (GET /clients/:id/).
    Includes a nested list of projects associated with the client.
    """
    projects = ProjectListSerializer(many=True, read_only=True, help_text="List of projects associated with this client.")
    
    class Meta(ClientSerializer.Meta):
        # Inherit fields from ClientSerializer and add 'projects'
        fields = ClientSerializer.Meta.fields + ['projects']