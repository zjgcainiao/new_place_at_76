from .base import JsonResponse, stripe, render, InternalUser, CustomerUser, logger
import uuid

# this is a utility function to check the number of searches a user has made by reading the "user_uuid" key from the session
# for un-authorized users.


def manage_vehicle_search_limit(user, session, search_type, search_success, manual_max_set=0):
    """
    Manages the vehicle search limit for a user session.
    :param user: User object or None for anonymous users
    :param session: Session dict to access or modify session data
    :param search_type: str, type of the search ('action_vin_search' or 'action_plate_search')
    :param search_success: bool, indicates if the search was successful
    :return: tuple (bool, dict), first element indicates if the limit is reached, 
             second element is the context for response
    """

    MAX_VIN_SEARCHES = 6
    MAX_LICENSE_PLATE_SEARCHES = 3
    MAX_VIN_SEARCHES_FOR_INTERNAL_USER = 200
    MAX_LICENSE_PLATE_SEARCHES_FOR_INTERNAL_USER = 200
    MAX_VIN_SEARCHES_FOR_CUSTOMER_USER = 10
    MAX_LICENSE_PLATE_SEARCHES_FOR_CUSTOMER_USER = 5
    logger.info(
        f'managing vehicle search limit for search_type: {search_type}...search_success: {search_success}...manual_max_set: {manual_max_set}...')
    # nested function to get the search limit key

    def get_search_limit_key(search_type, user):
        if user and user.is_authenticated:
            if isinstance(user, InternalUser):
                return f"{search_type}_for_internal_user"
            elif isinstance(user, CustomerUser):
                return f"{search_type}_for_customer_user"
        return search_type

    search_type_key = get_search_limit_key(search_type, user)

    search_limits = {
        'action_vin_search':   MAX_VIN_SEARCHES if manual_max_set == 0 else manual_max_set,
        'action_plate_search': MAX_LICENSE_PLATE_SEARCHES if manual_max_set == 0 else manual_max_set,
        'action_vin_search_for_internal_user':   MAX_VIN_SEARCHES_FOR_INTERNAL_USER,
        'action_plate_search_for_internal_user': MAX_LICENSE_PLATE_SEARCHES_FOR_INTERNAL_USER,
        'action_vin_search_for_customer_user':   MAX_VIN_SEARCHES_FOR_CUSTOMER_USER,
        'action_plate_search_for_customer_user': MAX_LICENSE_PLATE_SEARCHES_FOR_CUSTOMER_USER,
    }
    # dynamically generate max search count
    max_searches = search_limits.get(search_type_key, None)
    if max_searches is None:
        raise ValueError('Invalid search type provided')
    logger.info(
        f'the search_type_key is set: {search_type_key}..its max search count is: {max_searches}...')
    # Set search_count_key based on search_type
    if 'vin' in search_type_key:
        search_count_key = 'vin_search_count'
    elif 'plate' in search_type_key:
        search_count_key = 'license_plate_search_count'
    else:
        raise ValueError('Invalid search type provided')

    # Use a different key for authenticated users
    # to separate their count from anonymous users
    if user and user.is_authenticated:
        search_count_key = f'signed_in_user_{user.pk}_{search_count_key}'

    else:
        # Handle anonymous users
        if not session.get('anonymous_user_uuid'):
            user_uuid = uuid.uuid4()
            session['anonymous_user_uuid'] = str(user_uuid)
        else:
            user_uuid = session.get('anonymous_user_uuid')
        # Use a different search_count_key for anonymous users
        search_count_key = f'anonymous_user_{user_uuid}_{search_count_key}'

    # Retrieve current search count
    search_count = session.get(search_count_key, 0)

    if search_success and search_count < max_searches:
        # Increment the search count
        logger.info(
            f'incrementing search count for {search_count_key}...new count: {search_count + 1}')
        session[search_count_key] = search_count + 1
        # Indicate that the limit is not reached
        return False, {'success': 'search request is granted successfully'}

    # If the limit is reached, prepare the context for the response
    context = {'error': 'You have reached the maximum number of allowed searches... \
                    If you have not created an account, please create one to continue searching.',
               'show_login_link': True,
               }
    return True, context
