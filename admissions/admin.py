from django.contrib import admin
from .models import Application, AdminRequest


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'program', 'status', 'submitted_at']
    list_filter = ['status', 'program', 'submitted_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['id', 'submitted_at', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('program')


@admin.register(AdminRequest)
class AdminRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'status', 'requested_at', 'reviewed_by']
    list_filter = ['status', 'requested_at', 'reviewed_at']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['id', 'requested_at', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'reviewed_by')