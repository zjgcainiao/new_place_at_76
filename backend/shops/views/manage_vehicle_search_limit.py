from .base import JsonResponse, stripe, render, InternalUser, CustomerUser, \
        uuid


# this is a utility function to check the number of searches a user has made by reading the "user_uuid" key from the session
# for un-authorized users.

def manage_vehicle_search_limit(request, max_searches=1):
    """
    Manages the vehicle search limit for a request.
    :param request: HttpRequest object
    :param max_searches: int, maximum number of searches allowed
    :return: tuple (bool, dict), first element indicates if the limit is reached, 
             second element is the context for response
    """
    
    # Default search count
    search_count = 0

    # Default key for search count in session
    search_count_key = 'vehicle_search_count'

    # Adjust max_searches based on user type
    if request.user.is_authenticated:
        if isinstance(request.user, InternalUser):
            max_searches = 10
        elif isinstance(request.user, CustomerUser):
            max_searches = 3

        # Use a different key for authenticated users to separate their count from anonymous users
        search_count_key = f'user_{request.user.pk}_{search_count_key}'

    else:
        # For anonymous users, check if the user_uuid exists, if not, create one
        if not request.session.get('user_uuid'):
            request.session['user_uuid'] = str(uuid.uuid4())
            request.session[search_count_key] = search_count

    # Retrieve current search count
    search_count = request.session.get(search_count_key, 0)

    if search_count < max_searches:
        # Increment the search count
        request.session[search_count_key] = search_count + 1
        return False, {}  # Indicate that the limit is not reached

    # If the limit is reached, prepare the context for the response
    context = {'error': 'You have reached the maximum number of allowed vehicle searches... \
                    If you have not created an account, please create one to continue searching.',
               'show_login_link': True,
               }
    return True, context
