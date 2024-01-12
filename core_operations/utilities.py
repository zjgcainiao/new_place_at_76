import logging
from django.db import connections
from django.db.utils import OperationalError
# from customer_users.models import CustomerUser
# from internal_users.models import InternalUser


logger = logging.getLogger("django_db")

# this function is used to test the connection to the database. enable `python manage.py shell` terminal first. and then run this function.
# if the database connection is successful, it will return True. otherwise, it will return False.
def test_db_connection():
    """
    Test the connection to the application-used database.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        db_conn = connections['default']
        db_conn.cursor()
    except OperationalError:
        logger.exception("Unable to connect to the application-used database.")
        return False
    else:
        logger.info("Django Database connection is successful.")
        return True

# 2023-12-27. this function takes in a request object and returns the client's ip address. 
# ulitity function to get client ip address
def get_client_ip(request):
    """
    Get the client's IP address from the request object.

    Args:
        request (HttpRequest): The request object.

    Returns:
        str: The client's IP address.

    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # In case of proxies, grab the first IP
    else:
        ip = request.META.get('REMOTE_ADDR')  # Direct IP address
    return ip

# utility function to anonymize ip address
def anonymize_ip(ip):
    """
    Anonymizes the given IP address by replacing the last octet with '0'.

    Args:
        ip (str): The IP address to be anonymized.

    Returns:
        str: The anonymized IP address.

    """
    if ip:
        parts = ip.split('.')
        if len(parts) == 4:  # For IPv4
            parts[3] = '0'
        return '.'.join(parts)
    return ip


# get_user_details function is used to get the user details.

def get_user_details(request):
    is_authenticated = request.user.is_authenticated or False

            
    return {
        "is_authenticated": request.user.is_authenticated,
        # Add other user details you need
    }
