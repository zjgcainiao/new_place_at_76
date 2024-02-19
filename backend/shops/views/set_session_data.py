from .base import database_sync_to_async, render


@database_sync_to_async
def set_session_data(request, key, data):
    """
    Sets the session data with the specified key and data.
    """
    request.session[key] = data
    request.session.modified = True  # Ensure the session is saved


