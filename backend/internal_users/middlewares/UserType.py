from .base import SimpleLazyObject, get_user_model, InternalUser, CustomerUser, FirebaseUser, logger

# Example of using the User variable
# User = get_user_model()
# user_instance = User.objects.get(email='example@example.com')

def add_user_type_to_user(user):
    if not user.is_authenticated:
        return user  # Return the original user if not authenticated
    # if user.user_type:
    #     return user
      # Check if user_type has already been added to avoid re-adding it
    if getattr(user, 'user_type', None) is not None:
        return user
    
    # Dynamically determine user type based on model instance type
    if isinstance(user, InternalUser):
        user.user_type = 'InternalUser'
        logger.info(f'User Type: InternalUser has been added to the user instance.')
    elif isinstance(user, CustomerUser):
        user.user_type = 'CustomerUser'
        logger.info(f'User Type: CustomerUser has been added to the user instance.')
    elif isinstance(user, FirebaseUser):
        user.user_type = 'FirebaseUser'
        logger.info(f'User Type: FirebaseUser has been added to the user instance.')
    else:
        user.user_type = 'Unknown'
        logger.info(f'User Type: Unknown. A new field "user_type" has been added to the user instance.')
    return user

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture the current user object to avoid recursion
        current_user = request.user
        # Wrap request.user with SimpleLazyObject to avoid database hits until necessary
        request.user = SimpleLazyObject(lambda: add_user_type_to_user(current_user))
        response = self.get_response(request)
        return response
    