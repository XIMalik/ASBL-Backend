import uuid
from django.db import models
from django.core.validators import EmailValidator
from core.models import Program, Profile


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='applications')
    personal_statement = models.TextField()
    goals = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    documents = models.JSONField(default=list)
    identification_type = models.TextField(blank=True, null=True)
    identification_document_url = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications'
        indexes = [
            models.Index(fields=['program']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program.name}"


class AdminRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(validators=[EmailValidator()])
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_admin_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admin_requests'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Admin request from {self.email} ({self.status})"