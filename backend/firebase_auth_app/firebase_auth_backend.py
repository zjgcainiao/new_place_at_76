
from django.contrib.auth.backends import BaseBackend
from internal_users.models import InternalUser
from firebase_admin import auth
import time
import json
import logging
from django.contrib import messages
from firebase_auth_app.models import FirebaseUser
logger = logging.getLogger('django')

class FirebaseAuthBackend(BaseBackend):

    def authenticate(self, request, token, **kwargs):
        # if request.method == 'POST':      
        if token is None:
            return None      
        try:
            decoded_token = auth.verify_id_token(token)

            exp = decoded_token['exp']
            # Check token expiration

            if exp < time.time():
                messages.error(request, f'Error! Token expired. Please log in again.')
                return None
            uid=decoded_token['uid']
            return FirebaseUser.objects.get_or_create(uid=uid,
                                                    )[0]
        except auth.InvalidIdTokenError:
            return None
    
    def get_user(self, uid):
        try:
            # user =auth.get_user(uid)
            user = FirebaseUser.objects.get(uid=uid)
            return user
        except FirebaseUser.DoesNotExist:
            return None

