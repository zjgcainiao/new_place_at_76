
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
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions
from .firebase_auth_backend import FirebaseAuthBackend
import logging
import time
from firebase_admin.exceptions import FirebaseError, UnauthenticatedError, ResourceExhaustedError
import jwt

logger = logging.getLogger('django')


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token_type = request.headers.get('Token-Type')
        token = request.headers.get('Authorization')
        # if token_type == 'firebase':
        logger.info(
            f'Token fetched from http request: {token}...token_type: {token_type}')
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
        token = request.headers.get('Authorization')
        token_type = request.headers.get('Token-Type')
        if token and token.startswith('Bearer '):
            token = token.split('Bearer ')[1]

        logger.info(
            f'Token fetched from http request: {token}...token_type: {token_type}')
        print(
            f'Token fetched from http request: {token}...token_type: {token_type}')

        if not token or not token_type:
            return None

        if token_type == 'firebase':
            try:
                user = FirebaseAuthBackend().authenticate(request, token=token)
                logger.info(
                    f'User authentication via firebase token: {user}')
                if user is not None:
                    return (user, None)  # authentication successful
            except NoAuthToken as e:
                raise Exception('No authentication token provided') from e
            except InvalidAuthToken as e:
                raise Exception('Invalid authentication token') from e
            except FirebaseError as e:
                raise Exception('Firebase authentication error') from e

            except exceptions.AuthenticationFailed:
                raise Exception(f'Firebase authentication failed: {e}')

        # token_type = simplejwt, try SimpleJWT
        elif token_type == 'simplejwt':
            # Validate the token
            try:
                # This will check against the token's validity and relevant user
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                raise exceptions.AuthenticationFailed(
                    'Invalid token') from e

            # Get the user from the validated token
            jwt_user = self.get_user_from_token(token)
            logger.info(
                f'User authentication via JWTAuthentication: {jwt_user}')

            if jwt_user:
                return jwt_user, True  # JWT user authenticated
            else:
                raise exceptions.AuthenticationFailed('User not found')
        else:
            logger.error(
                f'Both Firebase and SimpleJWT Authentications failed for token: {token} and token_type: {token_type}')
            return None, False
        # If both methods fail, authentication is not provided
        return None, None

    def get_user_from_token(self, token):
        # Decode the token to get user_id
        try:
            decoded_data = jwt.decode(token,
                                      api_settings.SIGNING_KEY,
                                      algorithms=[
                                          api_settings.ALGORITHM]
                                      )
            user_id = decoded_data['user_id']
            print(f'User ID from decoded jwt token: {user_id}')
            # Or however you reference the user in your token
            return CustomerUser.objects.get(id=user_id)
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed(
                'Error decoding token') from e
        except CustomerUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist')
