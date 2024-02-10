from .base import SimpleLazyObject, get_user_model, InternalUser, CustomerUser, FirebaseUser, logger

# Example of using the User variable
# User = get_user_model()
# user_instance = User.objects.get(email='example@example.com')

def add_user_type_to_user(user):
    if not user.is_authenticated:
        return user  # Return the original user if not authenticated

    # Dynamically determine user type based on model instance type
    if isinstance(user, InternalUser):
        user.user_type = 'InternalUser'
        logger.info(f'User Type: InternalUser.A new field "user_type" has been added to the user instance.')
    elif isinstance(user, CustomerUser):
        user.user_type = 'CustomerUser'
        logger.info(f'User Type: CustomerUser.A new field "user_type" has been added to the user instance.')
    elif isinstance(user, FirebaseUser):
        user.user_type = 'FirebaseUser'
        logger.info(f'User Type: FirebaseUser. A new field "user_type" has been added to the user instance.')
    else:
        user.user_type = 'Unknown'
        
    
    return user

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Wrap request.user with SimpleLazyObject to avoid database hits until necessary
        request.user = SimpleLazyObject(lambda: add_user_type_to_user(request.user))
        response = self.get_response(request)
        return response