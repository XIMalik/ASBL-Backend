from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProgramViewSet, PersonViewSet, ProgramPersonViewSet, NewsViewSet, HealthCheck
from .auth_views import login, register

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'people', PersonViewSet)
router.register(r'program-people', ProgramPersonViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', login, name='login'),
    path('api/auth/register/', register, name='register'),
    path('api/health-check/', HealthCheck.as_view(), name='health-check'),
]