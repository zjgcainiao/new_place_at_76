
from math import e
from rest_framework.authentication import BaseAuthentication
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from rest_framework import authentication
from datetime import timezone
from .exceptions import NoAuthToken, InvalidAuthToken
from customer_users.models import CustomerUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from .firebase_auth_backend import FirebaseAuthBackend
import logging
import time
from firebase_admin.exceptions import FirebaseError, UnauthenticatedError, ResourceExhaustedError

logger = logging.getLogger('django')


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise NoAuthToken('No authentication token provided')
        if not token.startswith('Bearer '):
            raise InvalidAuthToken('Invalid authentication token')
        token = token.split('Bearer ')[1]
        try:
            decoded_token = auth.verify_id_token(token)
            exp = decoded_token['exp']
            # Check token expiration
            if exp < time.time():
                raise InvalidAuthToken('Token expired')
            uid = decoded_token['uid']
            user = CustomerUser.objects.get(firebase_uid=uid)
            return (user, None)
        except UnauthenticatedError:
            raise FirebaseError('Invalid Firebase authentication token',
                                'Invalid Firebase authentication token')
        except CustomerUser.DoesNotExist:
            raise FirebaseError('Firebase user not found',
                                'Firebase user not found')


class FirebaseAndSimpleJwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        # if token and token.startswith('Bearer '):
        #     token = token.split('Bearer ')[1]
        logger.info(f'token fetched from http request: {token}')
        logger.info(f'FirebaseAndSimpleJwtAuthentication token: {token}')
        if not token:
            return None
        try:
            user = FirebaseAuthBackend().authenticate(request, token=token)
            logger.info(
                f'User authentication via FirebaseAuthBackend: {user}')
            if user is not None:
                return (user, None)  # authentication successful
        # except NoAuthToken:
        #     raise Exception('No authentication token provided')
        # except InvalidAuthToken:
        #     raise Exception('Invalid authentication token')
        # except FirebaseError as e:
        #     raise Exception('Firebase authentication error') from e

        except exceptions.AuthenticationFailed:
            pass  # Ignore Firebase auth failures and try SimpleJWT next

        # If Firebase auth fails, try SimpleJWT

        jwt_auth = JWTAuthentication()
        logger.info(
            f'Firebase authentication failed. Trying SimpleJWT next..{jwt_auth}')
        try:
            jwt_user = jwt_auth.authenticate(request)
            logger.info(
                f'User authentication via JWTAuthentication: {jwt_user}')
            if jwt_user:
                return jwt_user  # JWT user authenticated
        except exceptions.AuthenticationFailed:
            logger.info(
                f'Both Firebase and SimpleJWT authentication failed')
            pass  # Ignore SimpleJWT auth failures

        # If both methods fail, authentication is not provided
        return None
