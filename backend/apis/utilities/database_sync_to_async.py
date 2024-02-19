
from .base import models, VinNhtsaApiSnapshots, sync_to_async,close_old_connections,DatabaseError,IntegrityError

# this is a custom version of sync_to_async function that explcitly control database connections
# 1. manages the connection's lifecycle expliclty, ensure that connections are properly closed afer usage.
# 2. i can add logiging speicifc to database operations.
# 3. can cutomize common database exceptions uniformly.
def database_sync_to_async(func):
    """
    Turn a sync function that interacts with the database into an async function.
    Handles database connection management and common exception handling.
    """

    @sync_to_async
    def wrapper(*args, **kwargs):
        try:
            # Ensure old DB connections are closed
            close_old_connections()
            # Execute the function
            result = func(*args, **kwargs)
            return result

        except DatabaseError as de:
            # You can log the exception, take corrective actions or re-raise
            # For now, I'm just re-raising
            raise de

        except IntegrityError as ie:
            # Handle integrity errors, e.g., unique constraint violations
            # Again, you can log, correct or re-raise
            raise ie
        except Exception as e:
            # Handle common database exceptions if required.
            # For example: handle DatabaseError, IntegrityError, etc.
            # You can log the exception or take other corrective actions.
            raise e
        finally:
            # Ensure old DB connections are closed after function execution
            close_old_connections()

    return wrapper


