from rest_framework import serializers
from .models import Application, AdminRequest


class ApplicationSerializer(serializers.ModelSerializer):
    program_name = serializers.StringRelatedField(source='program', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'program', 'program_name',
                 'personal_statement', 'goals', 'status', 'documents',
                 'identification_type', 'identification_document_url', 
                 'submitted_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'submitted_at', 'created_at', 'updated_at']

class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class AdminRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField()
    
    class Meta:
        model = AdminRequest
        fields = ['id', 'email', 'first_name', 'last_name', 'status', 'user', 
                 'requested_at', 'reviewed_at', 'reviewed_by', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'requested_at', 'created_at', 'updated_at']