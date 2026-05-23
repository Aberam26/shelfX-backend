"""
Custom DRF exception handler and authentication backend.
"""

import bcrypt
from rest_framework.views import exception_handler
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


def custom_exception_handler(exc, context):
    """Custom exception handler that wraps DRF errors in our API format."""
    response = exception_handler(exc, context)

    if response is not None:
        # If it's a validation error with detail as a dict, format as 'errors'
        if isinstance(response.data, dict) and 'detail' in response.data:
            response.data = {
                'success': False,
                'message': str(response.data['detail']),
            }

    return response


class EmailBackend(ModelBackend):
    """
    Authenticate using email instead of username.
    Also handles Laravel's $2y$ bcrypt hashes by converting to $2b$.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # Get the raw password hash from the database
        raw_hash = user.password

        # Handle Laravel's $2y$ bcrypt hashes
        if raw_hash.startswith('$2y$') or raw_hash.startswith('$2b$'):
            # Convert $2y$ to $2b$ (algorithmically identical)
            check_hash = raw_hash.replace('$2y$', '$2b$', 1) if raw_hash.startswith('$2y$') else raw_hash
            try:
                if bcrypt.checkpw(password.encode('utf-8'), check_hash.encode('utf-8')):
                    return user
            except (ValueError, TypeError):
                pass
            return None

        # Fall back to Django's standard password checking
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
