from rest_framework import serializers
from .models import Application, AdminRequest


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'program',
                 'personal_statement', 'goals', 'status', 'documents',
                 'identification_type', 'identification_document_url', 
                 'submitted_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'submitted_at', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Replace program ID with program name
        representation['program'] = instance.program.name
        return representation

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