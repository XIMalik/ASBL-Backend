from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import os
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Application, AdminRequest
from .serializers import ApplicationSerializer, AdminRequestSerializer
from core.models import Profile


class IsOwnerOrAdminOrReviewer(permissions.BasePermission):
    """Custom permission: Users can access own data, admins/reviewers can access all"""
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            if profile.role in ['admin', 'reviewer']:
                return True
            # Users can only access their own applications
            if hasattr(obj, 'email'):
                return obj.email == profile.email
        return False


@extend_schema_view(
    list=extend_schema(
        summary="List applications",
        description="Get list of student applications. Users see only their own, admins/reviewers see all.",
        tags=["Applications"]
    ),
    create=extend_schema(
        summary="Submit application",
        description="Submit a new student application to a program. Anyone can submit applications.",
        tags=["Applications"]
    ),
    retrieve=extend_schema(
        summary="Get application details",
        description="Retrieve detailed information about a specific application.",
        tags=["Applications"]
    ),
    update=extend_schema(
        summary="Update application",
        description="Update application information. Users can update own applications, admins can update any.",
        tags=["Applications"]
    ),
    destroy=extend_schema(
        summary="Delete application",
        description="Delete an application. Only admins can delete applications.",
        tags=["Applications"]
    )
)

class DocumentUploadView(APIView):
    permission_classes = [permissions.AllowAny]  # or IsAuthenticated

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ext = os.path.splitext(file.name)[1]
        filename = f"applications/{uuid.uuid4()}{ext}"

        path = default_storage.save(filename, ContentFile(file.read()))
        file_url = request.build_absolute_uri(
            default_storage.url(path)
        )

        return Response(
            {'url': file_url},
            status=status.HTTP_201_CREATED
        )

class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing student applications"""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            # Anyone can create applications
            return [permissions.AllowAny()]
        return [IsOwnerOrAdminOrReviewer()]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            if profile.role in ['admin', 'reviewer']:
                return Application.objects.all()
            # Users can only see their own applications
            return Application.objects.filter(email=profile.email)
        return Application.objects.none()
    
    @extend_schema(
        summary="Update application status",
        description="Update the status of an application (pending, approved, rejected). Only admins and reviewers can update status.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'enum': ['pending', 'approved', 'rejected'],
                        'description': 'New status for the application'
                    }
                },
                'required': ['status']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'Status updated successfully'}
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Invalid status'}
                }
            },
            403: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Permission denied'}
                }
            }
        },
        tags=["Applications"]
    )
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        application = self.get_object()
        if not (hasattr(request.user, 'profile') and request.user.profile.role in ['admin', 'reviewer']):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status in ['pending', 'approved', 'rejected']:
            application.status = new_status
            application.save()
            return Response({'status': 'Status updated successfully'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="List admin requests",
        description="Get list of admin privilege requests. Users see only their own, admins see all.",
        tags=["Admin Requests"]
    ),
    create=extend_schema(
        summary="Request admin privileges",
        description="Submit a request for admin privileges. Only authenticated users can make requests.",
        tags=["Admin Requests"]
    ),
    retrieve=extend_schema(
        summary="Get admin request details",
        description="Retrieve detailed information about a specific admin request.",
        tags=["Admin Requests"]
    ),
    update=extend_schema(
        summary="Update admin request",
        description="Update admin request information.",
        tags=["Admin Requests"]
    ),
    destroy=extend_schema(
        summary="Delete admin request",
        description="Delete an admin request. Only admins can delete requests.",
        tags=["Admin Requests"]
    )
)
class AdminRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing admin privilege requests"""
    queryset = AdminRequest.objects.all()
    serializer_class = AdminRequestSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            if profile.role == 'admin':
                return AdminRequest.objects.all()
            # Users can only see their own admin requests
            return AdminRequest.objects.filter(email=profile.email)
        return AdminRequest.objects.none()
    
    @extend_schema(
        summary="Review admin request",
        description="Approve or reject an admin privilege request. Only admins can review requests.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'enum': ['approved', 'rejected'],
                        'description': 'Decision on the admin request'
                    }
                },
                'required': ['status']
            }
        },

        responses={
            200: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'Request reviewed successfully'}
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Invalid status'}
                }
            },
            403: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Only admins can review requests'}
                }
            }
        },
        tags=["Admin Requests"]
    )
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def review(self, request, pk=None):
        admin_request = self.get_object()
        if not (hasattr(request.user, 'profile') and request.user.profile.role == 'admin'):
            return Response({'error': 'Only admins can review requests'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status in ['approved', 'rejected']:
            admin_request.status = new_status
            admin_request.reviewed_at = timezone.now()
            admin_request.reviewed_by = request.user.profile
            admin_request.save()
            
            # If approved, update user role
            if new_status == 'approved' and admin_request.user:
                admin_request.user.role = 'admin'
                admin_request.user.save()
            
            return Response({'status': 'Request reviewed successfully'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)