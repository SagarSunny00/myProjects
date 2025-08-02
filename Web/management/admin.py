# management/admin.py

from django.contrib import admin
from .models import Client, Project

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Client model.    """
    list_display = ('client_name', 'created_at', 'created_by', 'updated_at', 'updated_by')
    search_fields = ('client_name',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by') # These fields are system-managed

    def save_model(self, request, obj, form, change):
        """
        Override save_model to automatically set created_by and updated_by
        when objects are created/updated via the Django Admin.
        """
        if not obj.pk: # Object is being created for the first time
            obj.created_by = request.user
        obj.updated_by = request.user # Always update on save
        super().save_model(request, obj, form, change)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.
    """
    list_display = ('name', 'client', 'display_users', 'created_at', 'created_by', 'updated_at', 'updated_by')
    list_filter = ('client', 'users')
    search_fields = ('name',)
    filter_horizontal = ('users',) # Provides a nice interface for ManyToMany field
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def display_users(self, obj):
        """Helper to display assigned users as a comma-separated string."""
        return ", ".join([user.username for user in obj.users.all()])
    display_users.short_description = 'Assigned Users' # Column header in admin list

    def save_model(self, request, obj, form, change):
        """
        Override save_model to automatically set created_by and updated_by
        when objects are created/updated via the Django Admin.
        """
        if not obj.pk: # Object is being created for the first time
            obj.created_by = request.user
        obj.updated_by = request.user # Always update on save
        super().save_model(request, obj, form, change)