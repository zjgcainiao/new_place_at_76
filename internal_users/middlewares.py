
from django.http import HttpResponseForbidden
from internal_users.models import InternalUser
from django.shortcuts import redirect
from customer_users.models import CustomerUser
from django.urls import resolve, reverse
import os


class InternalUserMiddleware:
    # Define apps that need to pass through the middleware check
    PROTECTED_APPS = ['talents', 'apis',
                      'dashboard', 'admin', 'talent_management', 'appointments', 'customer_users']

    # login_url = reverse('internal_users:internal_user_login')

    def __init__(self, get_response):
        self.get_response = get_response
        self.employee_login_url = reverse('internal_users:internal_user_login')
        self.customer_login_url = reverse('customer_users:customer_user_login')

    def __call__(self, request):
        # Resolve the current app name
        current_app = resolve(request.path_info).app_name
        print(
            F'The current_app name is {current_app}. current_request_url is {request.path}. User is_authenticated: {request.user.is_authenticated}')

        # print(request.path, request.user.is_authenticated)

        # If the user is trying to access the login page itself, bypass further checks
        if request.path == self.employee_login_url or request.path == self.customer_login_url:
            return self.get_response(request)

        # Check if the request path resolves to any of the protected apps
        if current_app in self.PROTECTED_APPS:
            print(
                f'url visit to protected app(s). Implementing custom rules in InternalUserMiddleware...')
            if not request.user.is_authenticated or (request.user.is_authenticated and not isinstance(request.user, InternalUser)):
                print('incorrect redirecting to the employee login url...')
                return redirect(self.employee_login_url)

            # Additional check for CustomerUser when visiting the customer_users app
            if current_app in ['customer_users'] and (not request.user.is_authenticated or (request.user.is_authenticated and not isinstance(request.user, CustomerUser))):
                # Redirect to the customer user login
                print('redirecting to the customer login url...')
                return redirect(self.customer_login_url)

        return self.get_response(request)
