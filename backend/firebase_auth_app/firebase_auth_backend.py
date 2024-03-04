
from django.contrib.auth.backends import BaseBackend
from apis.serializers import phone
from internal_users.models import InternalUser
from firebase_admin import auth
import time
import json
import logging
from django.contrib import messages
from firebase_auth_app.models import FirebaseUser  # not currently in use
from customer_users.models import CustomerUser
from firebase_admin.exceptions import FirebaseError, UnauthenticatedError, ResourceExhaustedError

logger = logging.getLogger('django')


class FirebaseAuthBackend(BaseBackend):

    def authenticate(self, request, token, **kwargs):
        # if request.method == 'POST':
        if token is None:
            return None
        try:
            decoded_token = auth.verify_id_token(token)
            logger.info(
                f'the token decoded via firebaseAuthBackend looks like : {decoded_token}')
            exp = decoded_token['exp']
            # Check token expiration
            print(f'the decoded firebase token expiration time is : {exp}')
            if exp < time.time():
                messages.error(
                    request, f'Error! Token expired. Please log in again.')
                return None
            uid = decoded_token['uid']
            # phone_number = decoded_token['phone_number']
            customer_user = CustomerUser.objects.get_or_create(
                firebase_uid=uid, cust_user_email=decoded_token['email'])[0]
            return customer_user

        except UnauthenticatedError:
            return None

    def get_user(self, uid):
        try:
            # user =auth.get_user(uid)
            user = CustomerUser.objects.get(firebase_uid=uid)
            return user
        except CustomerUser.DoesNotExist:
            return None
