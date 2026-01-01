from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, AdminRequestViewSet, DocumentUploadView

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'admin-requests', AdminRequestViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload-document/', DocumentUploadView.as_view(), name='upload-document'),
]