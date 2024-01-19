
import os
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from internal_users.models import InternalUser
from firebase_auth_app.models import FirebaseUser
from customer_users.models import CustomerUser
from django.contrib import messages

class InternalUserMiddleware:
    # Define apps that need to pass through the middleware check
    PROTECTED_APPS = ['talents','dashboard', 'admin', 'talent_management',]  # 'appointments'
    PROTECTED_CUSTOMER_APPS = ['customer_users',]  # 'appointments'

    # login_url = reverse('internal_users:internal_user_login')

    def __init__(self, get_response):
        self.get_response = get_response
        self.employee_login_url = reverse('internal_users:internal_user_login')
        self.employee_register_url = reverse('internal_users:internal_user_register')
        self.employee_logout_url = reverse('internal_users:internal_user_logout')
        self.customer_login_url = reverse('customer_users:customer_user_login')
        self.customer_logout_url = reverse('customer_users:customer_user_logout')
        self.customer_register_url = reverse('customer_users:customer_user_register')
        self.customer_profile = reverse('customer_users:customer_user_profile')

    def __call__(self, request):
        # Resolve the current app name
        current_app = resolve(request.path_info).app_name
        # print(
        #     F'The current_app name is {current_app}. url requseted is {request.path}. is_authenticated?:{request.user.is_authenticated}.')

        # print(request.path, request.user.is_authenticated)

        # If the user is trying to access the login page itself, bypass further checks
        if request.path in [self.customer_login_url,self.employee_logout_url, self.customer_login_url,self.customer_logout_url,
                            self.customer_register_url,self.employee_register_url]:
            return self.get_response(request)

        # Check if the request path resolves to any of the protected apps
        if current_app in self.PROTECTED_APPS:
            print(f'url visit to protected app(s). Implementing custom rules in InternalUserMiddleware...')

            if not request.user.is_authenticated:
                messages.error(request, f'Employee Login Required.')
                print('user not logged in . Redirecting to the employee login url...')
                return redirect(self.employee_login_url)
            elif request.user.is_authenticated and isinstance(request.user, CustomerUser):   
                return redirect(self.customer_logout_url)
            # elif request.user.is_authenticated and isinstance(request.user, InternalUser):
                
            #     return redirect(self.employee_login_url)
    
        if current_app in self.PROTECTED_CUSTOMER_APPS:
            print(f'url visit to protected customer app(s). Implementing custom rules in InternalUserMiddleware...')
            # # Additional check for CustomerUser when visiting the customer_users app
            if not request.user.is_authenticated:
                messages.error(request, f'Error. Customer Login Required. Please Login. Create a new account if you do not have one.')
                return redirect(self.customer_login_url)
            elif request.user.is_authenticated and isinstance(request.user, InternalUser):
                # Redirect to the customer user login
                messages.error(request, f'Error! Please log out your employee account before visiting this page.')
                print('redirecting to the customer login url...')
                return redirect(self.employee_logout_url)
            
        return self.get_response(request)



# the future used multiple user model authentication middleware; designed used with firebase auth

class MultipleUserModelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'uid' in request.session:
            uid = request.session['uid']
            firebase_user = None
            specific_user = None

            try:
                firebase_user = FirebaseUser.objects.get(uid=uid)
            except FirebaseUser.DoesNotExist:
                pass

            if firebase_user:
                # Set base user
                request.firebase_user = firebase_user

                # Check each model to find the specific user
                for user_model in [CustomerUser, InternalUser]:
                    try:
                        specific_user = user_model.objects.get(
                            firebase_user=firebase_user)
                        break
                    except user_model.DoesNotExist:
                        continue

                if specific_user:
                    request.user = specific_user

        response = self.get_response(request)
        return response
