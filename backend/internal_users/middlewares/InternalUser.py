
import logging
from math import e
import time
from .base import reverse, resolve, redirect, messages, logger, InternalUser, CustomerUser
import json
from firebase_admin import auth
from django.http import JsonResponse
from firebase_auth_app.firebase_auth_backend import FirebaseAuthBackend
from django.contrib.auth import login


class InternalUserMiddleware:
    # Define apps that need to pass through the middleware check
    PROTECTED_APPS = ['talents', 'dashboard', 'admin',
                      'talent_management',]  # 'appointments'
    PROTECTED_CUSTOMER_APPS = ['customer_users',]  # 'appointments'

    # login_url = reverse('internal_users:internal_user_login')

    def __init__(self, get_response):
        self.get_response = get_response
        self.employee_login_url = reverse('internal_users:internal_user_login')
        self.employee_register_url = reverse(
            'internal_users:internal_user_register')
        self.employee_logout_url = reverse(
            'internal_users:internal_user_logout')
        self.customer_login_url = reverse('customer_users:customer_user_login')
        self.customer_logout_url = reverse(
            'customer_users:customer_user_logout')
        self.customer_register_url = reverse(
            'customer_users:customer_user_register')
        self.customer_profile = reverse('customer_users:customer_user_profile')
        self.customer_login_firebase_url = reverse(
            'customer_users:customer_user_login_firebaseauth')
        self.customer_register_firebase_url = reverse(
            'customer_users:customer_user_register_firebaseauth')
        self.customer_user_profile = reverse(
            'customer_users:customer_user_profile')
        self.verify_firebase_token = reverse(
            'firebase_auth_app:verify_firebase_token')

    def __call__(self, request):
        # Resolve the current app name
        current_app = resolve(request.path_info).app_name

        # if request.method == 'POST' and request.path in [self.customer_login_firebase_url,
        #                                                      self.customer_register_firebase_url,
        #                                                      self.verify_firebase_token]:
        #     # Access the raw JSON data from the request body
        #     try:
        #         data = json.loads(request.body)
        #                     # Extract required data from the parsed JSON
        #         token = data.get('token')
        #         uid = data.get('uid')
        #         new_user_flag = data.get('newUserFlag')
        #         user = auth.get_user(uid)
        #         request.user = user
        #     except json.JSONDecodeError:
        #         # Handle JSON decoding error
        #         logging.error('Invalid firebase user JSON data')
        #         input('Press Enter to continue...')

        #     return self.get_response(request)

        # If the user is trying to access the login page itself, bypass further checks
        if request.path in [self.customer_login_url,
                            self.customer_logout_url,
                            self.customer_login_firebase_url,
                            self.customer_register_firebase_url,
                            self.employee_login_url,
                            self.employee_logout_url,
                            self.customer_register_url,
                            self.employee_register_url
                            ]:
            return self.get_response(request)

        # Check if the request path resolves to any of the protected apps
        if current_app in self.PROTECTED_APPS:
            # logger.info(f'Implementing InternalUserMiddleware rules before visiting the protected app: \
            #             {current_app}.')

            if not request.user.is_authenticated:
                messages.error(request, f'Employee Login Required.')
                logger.warning(
                    'User is NOT logged in. Redirecting to the employee login url...')
                redirect_url = f"{self.employee_login_url}?next={request.path}"
                return redirect(redirect_url)
            elif request.user.is_authenticated and \
                    isinstance(request.user, CustomerUser):
                redirect_url = \
                    f"{self.customer_logout_url}?next={request.path}"
                return redirect(redirect_url)
            # elif request.user.is_authenticated and isinstance(request.user, InternalUser):

            #     return redirect(self.employee_login_url)

        if current_app in self.PROTECTED_CUSTOMER_APPS:
            logger.info(
                f'{current_app} is an protected app. Using customized rules...')
            print(f'user is authenticated: {request.user.is_authenticated}')

            try:
                session_data = request.session.get('firebase_data')
                if session_data:
                    firebase_data = json.loads(session_data)
                    uid = firebase_data['uid']
                    exp = firebase_data['exp']
            except Exception as e:
                logger.error(f'Error: {e}')
                uid = None
                exp = None

            # # Additional check for CustomerUser when visiting the customer_users app
            if not request.user.is_authenticated and not uid:
                messages.error(
                    request, f'Error. Customer Login Required. Please Login. Create a new account if you do not have one.')
                return redirect(self.customer_login_url)
            elif not request.user.is_authenticated and \
                    uid and exp > time.time():
                logger.info(
                    'Firebase user is authenticated. Proceed to the next middleware...')
                return self.get_response(request)
            # elif not request.user.is_authenticated and request.user.uid and request.user.exp < time.time():
            #     messages.error(request, f'Error! Token expired. Please log in again.')
            #     return redirect(self.customer_login_firebase_url)
            elif request.user.is_authenticated and isinstance(request.user, InternalUser):
                # Redirect to the customer user login
                messages.error(
                    request, f'Error! Please log out your employee account before visiting this page.')
                logger.info('redirecting to the customer login url...')
                return redirect(self.employee_logout_url)
            elif request.user.is_authenticated and isinstance(request.user, CustomerUser):
                logger.info(
                    'CustomerUser is authenticated. Proceed to the next middleware...')
                return self.get_response(request)

            else:
                messages.error(request, 'Error! Please log in again.')
                return redirect(self.customer_login_url)

        return self.get_response(request)
