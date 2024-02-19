import logging
from django.db import connections
from django.conf import settings
from django.db.utils import OperationalError
# from customer_users.models import CustomerUser
# from internal_users.models import InternalUser


logger = logging.getLogger("django.db")

# this function is used to test the connection to the database. enable `python manage.py shell` terminal first. and then run this function.
# if the database connection is successful, it will return True. otherwise, it will return False.
def test_db_connection():
    """
    Test the connection to the application-used database and log connection details.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    db_settings = settings.DATABASES['default']
    host = db_settings.get('HOST', 'Not specified')
    port = db_settings.get('PORT', 'Not specified')
    user = db_settings.get('USER', 'Not specified')
    database_name = db_settings.get('NAME', 'Not specified')
    
    try:
        db_conn = connections['default']
        db_conn.cursor()  # Attempt to create a cursor, implicitly opening a connection
    except OperationalError as e:
        logger.exception(f"Unable to connect to the application-used database. Error: {e}")
        logger.error(f"Failed connection details - Host: {host}, Port: {port}, User: {user}")
        return False
    else:
        logger.info("Django Database connection is successful.")
        print("Django Database connection is successful.")
        logger.info(f"Connection details - Host: {host}, Port: {port}, User: {user}")
        print(f"Connection details - Host: {host}, Port: {port}, Dataname {database_name}. User: {user}.SQL_DOCKERIZED {settings.SQL_DOCKERIZED}")
        return True
    finally:
        # Close the connection explicitly if it was opened
        if db_conn.connection:
            db_conn.close()

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


import json

def parse_raw_json(json_string):
    try:
        # Attempt to correct common formatting errors
        corrected_json_string = json_string.replace("'", '"')
        # Parse the corrected JSON string
        return json.loads(corrected_json_string)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return {}

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

def parse_to_two_digit_decimal(value):
    try:
        # Attempt to convert and round the value
        if value is not None:
            return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError) as e:
        # Log the error, adjust the logging as per your application's logging setup
        print(f"Error formatting decimal value '{value}': {e}")
    # Return None if there's an error or if the input value is None
    return None

from datetime import datetime

def format_date(date_str, date_format='%Y-%m-%d %H:%M:%S'):
    try:
        if date_str is not None:
            return datetime.strptime(date_str, date_format)
    except ValueError as e:
        # Log the error, adjust the logging as per your application's logging setup
        print(f"Error parsing date string '{date_str}': {e}")
    # Return None if there's an error or if the input date_str is None
    return None