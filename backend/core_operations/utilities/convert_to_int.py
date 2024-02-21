def convert_to_int(value_str, default=None):
    # Convert a string to an integer. If it's empty or not valid, return the default value."""
    try:
        return int(value_str)
    except (ValueError, TypeError):  # This handles both empty strings and other invalid values
        return default

