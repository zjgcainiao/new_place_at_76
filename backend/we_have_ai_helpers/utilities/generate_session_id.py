import uuid


def generate_session_id():
    return str(uuid.uuid4())  # Convert UUID to string for storage
