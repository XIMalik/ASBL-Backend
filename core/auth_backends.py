from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Profile


class ProfileAuthBackend(BaseBackend):
    """Custom authentication backend that links User to Profile"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            profile = Profile.objects.get(email=username)
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': username}
            )
            # Attach profile to user for easy access
            user.profile = profile
            return user
        except Profile.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            # Attach profile to user
            try:
                user.profile = Profile.objects.get(email=user.email)
            except Profile.DoesNotExist:
                pass
            return user
        except User.DoesNotExist:
            return None