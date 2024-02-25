
from rest_framework.authentication import BaseAuthentication
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from rest_framework import authentication
from datetime import timezone
from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError
from customer_users.models import CustomerUser

from .firebase_auth_backend import FirebaseAuthBackend

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            user = FirebaseAuthBackend().authenticate(request, token=token)
            if user is not None:
                return (user, None)  # authentication successful
        except NoAuthToken:
            raise Exception('No authentication token provided')
        except InvalidAuthToken:
            raise Exception('Invalid authentication token')
        except FirebaseError as e:
            raise Exception('Firebase authentication error') from e
