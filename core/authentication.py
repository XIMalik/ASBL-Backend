from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .models import Profile


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if user:
            try:
                user.profile = Profile.objects.get(email=user.email)
            except Profile.DoesNotExist:
                pass
        return user