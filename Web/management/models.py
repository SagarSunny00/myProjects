# management/models.py
from django.db import models
from django.contrib.auth.models import User  # Django's built-in User model

class Client(models.Model):
    """
    Represents a client in the system.
    A client can have multiple projects.
    """
    client_name = models.CharField(max_length=255, unique=True, help_text="Unique name for the client.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Link to the user who created/updated the client. Set to NULL if user is deleted.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_created', help_text="The user who created this client.")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_updated', help_text="The last user who updated this client.")
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['client_name']
    
    def __str__(self):
        return self.client_name

class Project(models.Model):
    """
    Represents a project, assigned to a client and can involve multiple users.
    """
    name = models.CharField(max_length=255, help_text="Name of the project.")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects', help_text="The client associated with this project.")
    users = models.ManyToManyField(User, related_name='projects', help_text="Users assigned to this project.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Link to the user who created/updated the project. Set to NULL if user is deleted.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_created', help_text="The user who created this project.")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_updated', help_text="The last user who updated this project.")
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        # Ensure a client cannot have two projects with the exact same name
        unique_together = ('name', 'client')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.client.client_name})"