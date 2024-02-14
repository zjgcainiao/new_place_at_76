
from .base import reverse, resolve, redirect, messages, logger, InternalUser, CustomerUser


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
        # If the user is trying to access the login page itself, bypass further checks
        if request.path in [self.customer_login_url,self.customer_logout_url,
                           self.employee_login_url, self.employee_logout_url, 
                            self.customer_register_url,self.employee_register_url
                            ]:
            return self.get_response(request)

        # Check if the request path resolves to any of the protected apps
        if current_app in self.PROTECTED_APPS:
            logger.info(f'Implementing InternalUserMiddleware rules before visiting the protected app:{current_app}.')

            if not request.user.is_authenticated:
                messages.error(request, f'Employee Login Required.')
                logger.warning('user not logged in . Redirecting to the employee login url...')
                redirect_url = f"{self.employee_login_url}?next={request.path}"
                return redirect(redirect_url)
            elif request.user.is_authenticated and isinstance(request.user, CustomerUser):   
                redirect_url = f"{self.customer_logout_url}?next={request.path}"
                return redirect(redirect_url)
            # elif request.user.is_authenticated and isinstance(request.user, InternalUser):
                
            #     return redirect(self.employee_login_url)
    
        if current_app in self.PROTECTED_CUSTOMER_APPS:
            logger.info(f' Implementing InternalUserMiddleware rules before visiting the {current_app} app...')
            # # Additional check for CustomerUser when visiting the customer_users app
            if not request.user.is_authenticated:
                messages.error(request, f'Error. Customer Login Required. Please Login. Create a new account if you do not have one.')
                return redirect(self.customer_login_url)
            elif request.user.is_authenticated and isinstance(request.user, InternalUser):
                # Redirect to the customer user login
                messages.error(request, f'Error! Please log out your employee account before visiting this page.')
                logger.info('redirecting to the customer login url...')
                return redirect(self.employee_logout_url)
            
        return self.get_response(request)

