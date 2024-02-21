# this function is used to test the connection to the database. enable `python manage.py shell` terminal first. and then run this function.
# if the database connection is successful, it will return True. otherwise, it will return False.
from .base import logger, settings, connections, OperationalError

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
