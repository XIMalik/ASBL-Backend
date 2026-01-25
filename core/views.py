from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from .models import Profile, Program, Person, ProgramPerson, News
from .serializers import (ProfileSerializer, ProgramSerializer, PersonSerializer, 
                         ProgramPersonSerializer, NewsSerializer)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission: Admin can modify, others can only read"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'admin'

@extend_schema_view(
    list=extend_schema(
        summary="List user profiles",
        description="Get list of user profiles. Admins see all profiles, users see only their own.",
        tags=["Profiles"]
    ),
    create=extend_schema(
        summary="Create user profile",
        description="Create a new user profile. Only admins can create profiles.",
        tags=["Profiles"]
    ),
    retrieve=extend_schema(
        summary="Get profile details",
        description="Retrieve details of a specific user profile.",
        tags=["Profiles"]
    ),
    update=extend_schema(
        summary="Update profile",
        description="Update user profile information.",
        tags=["Profiles"]
    ),
    destroy=extend_schema(
        summary="Delete profile",
        description="Delete a user profile. Only admins can delete profiles.",
        tags=["Profiles"]
    )
)
class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user profiles with role-based access"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin':
            return Profile.objects.all()
        return Profile.objects.filter(id=self.request.user.profile.id)

@extend_schema_view(
    list=extend_schema(
        summary="List academic programs",
        description="Get list of all academic programs available at the school.",
        tags=["Programs"]
    ),
    create=extend_schema(
        summary="Create program",
        description="Create a new academic program. Only admins can create programs.",
        tags=["Programs"]
    ),
    retrieve=extend_schema(
        summary="Get program details",
        description="Retrieve detailed information about a specific academic program.",
        tags=["Programs"]
    ),
    update=extend_schema(
        summary="Update program",
        description="Update academic program information. Only admins can update programs.",
        tags=["Programs"]
    ),
    destroy=extend_schema(
        summary="Delete program",
        description="Delete an academic program. Only admins can delete programs.",
        tags=["Programs"]
    )
)
class ProgramViewSet(viewsets.ModelViewSet):
    """ViewSet for managing academic programs"""
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @extend_schema(
        summary="Get program faculty",
        description="Retrieve all faculty members associated with this program.",
        responses=PersonSerializer(many=True),
        tags=["Programs"]
    )
    @action(detail=True, methods=['get'])
    def people(self, request, pk=None):
        program = self.get_object()
        people = Person.objects.filter(person_programs__program=program)
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(
        summary="List people",
        description="Get list of all faculty, mentors, and staff members.",
        tags=["People"]
    ),
    create=extend_schema(
        summary="Create person",
        description="Add a new faculty member, mentor, or staff. Only admins can create people.",
        tags=["People"]
    ),
    retrieve=extend_schema(
        summary="Get person details",
        description="Retrieve detailed information about a faculty member, mentor, or staff.",
        tags=["People"]
    ),
    update=extend_schema(
        summary="Update person",
        description="Update person information. Only admins can update people.",
        tags=["People"]
    ),
    destroy=extend_schema(
        summary="Delete person",
        description="Remove a person from the system. Only admins can delete people.",
        tags=["People"]
    )
)
class PersonViewSet(viewsets.ModelViewSet):
    """ViewSet for managing faculty, mentors, and staff"""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @extend_schema(
        summary="Get person's programs",
        description="Retrieve all programs associated with this person.",
        responses=ProgramSerializer(many=True),
        tags=["People"]
    )
    @action(detail=True, methods=['get'])
    def programs(self, request, pk=None):
        person = self.get_object()
        programs = Program.objects.filter(program_people__person=person)
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List program-person associations",
        description="Get list of all program-person relationships.",
        tags=["Program Associations"]
    ),
    create=extend_schema(
        summary="Create program-person association",
        description="Associate a person with a program. Only admins can create associations.",
        tags=["Program Associations"]
    ),
    destroy=extend_schema(
        summary="Remove program-person association",
        description="Remove association between a person and program. Only admins can remove associations.",
        tags=["Program Associations"]
    )
)
class ProgramPersonViewSet(viewsets.ModelViewSet):
    """ViewSet for managing program-person associations"""
    queryset = ProgramPerson.objects.all()
    serializer_class = ProgramPersonSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="List news articles",
        description="Get list of school news and announcements.",
        tags=["News"]
    ),
    create=extend_schema(
        summary="Create news article",
        description="Publish a new news article or announcement. Only admins can create news.",
        tags=["News"]
    ),
    retrieve=extend_schema(
        summary="Get news article",
        description="Retrieve a specific news article or announcement.",
        tags=["News"]
    ),
    update=extend_schema(
        summary="Update news article",
        description="Update news article content. Only admins can update news.",
        tags=["News"]
    ),
    destroy=extend_schema(
        summary="Delete news article",
        description="Delete a news article. Only admins can delete news.",
        tags=["News"]
    )
)
class NewsViewSet(viewsets.ModelViewSet):
    """ViewSet for managing school news and announcements"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = News.objects.all()
        if self.action == 'list' and not (hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin'):
            # Public users only see published news
            return queryset.order_by('-published_at')
        return queryset
    
    @extend_schema(
        summary="Get featured news",
        description="Retrieve all featured news articles and announcements.",
        responses=NewsSerializer(many=True),
        tags=["News"]
    )
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_news = News.objects.filter(featured=True).order_by('-published_at')
        serializer = self.get_serializer(featured_news, many=True)
        return Response(serializer.data)

class HealthCheck(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Health Check",
        description="Check if the API is running.",
        responses={200: OpenApiTypes.STR},
        tags=["Health"]
    )

    def get(self, request):
        return Response("Running.", status=status.HTTP_200_OK)