import logging
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger("django_db")

def test_db_connection():
    try:
        db_conn = connections['default']
        db_conn.cursor()
    except OperationalError:
        logger.exception("Unable to connect to the database.")
        return False
    else:
        logger.info("Database connection successful.")
        return True
