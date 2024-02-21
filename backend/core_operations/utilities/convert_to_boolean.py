
def convert_to_boolean(value_str, default=None):
    """Convert a string to a boolean. If it's empty or not recognized, return the default value."""
    truthy_values = ["true", "yes", "1", "active"]
    falsy_values = ["false", "no", "0", "inactive"]

    value_str_lower = value_str.lower().strip()

    if value_str_lower in truthy_values:
        return True
    elif value_str_lower in falsy_values:
        return False
    else:
        return default
