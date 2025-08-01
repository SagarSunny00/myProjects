from django.db import models

# Create your models here.

# Mangement/management/models.py

from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    client_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='clients_created'
    )

    def __str__(self):
        return self.client_name

    class Meta:
        ordering = ['-created_at']


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='projects'
    )
    users = models.ManyToManyField(User, related_name='projects_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='projects_created'
    )

    def __str__(self):
        return f"{self.project_name} ({self.client.client_name})"

    class Meta:
        ordering = ['-created_at']
        # A client cannot have two projects with the same name
        unique_together = ['project_name', 'client']
