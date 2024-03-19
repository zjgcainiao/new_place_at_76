


import json

def clean_string_in_dictionary_object(data):
    """Cleans strings within a dictionary-like object, providing more robust handling and error messages.

    Args:
        data (dict): The dictionary-like object to clean.

    Returns:
        dict: A cleaned version of the input dictionary.
    """

    cleaned_data = {}
    for key, value in data.items():
        if key is None:
            raise ValueError("Encountered None as a dictionary key, which is unexpected.")

        # Convert to string in case the key is not a string type.
        key_str = str(key)

        # Remove the BOM from the beginning of the key if it's there
        cleaned_key = key_str.lstrip('\ufeff')
        cleaned_key = cleaned_key.strip()
        cleaned_key = cleaned_key.replace('\u200b', '')  # Remove zero-width space
        
        if isinstance(value, str):
            try:
                # Attempt to load string as JSON (to handle potential quoted cases)
                potential_json = json.loads(value)
                if isinstance(potential_json, str):
                    cleaned_value = potential_json.strip()
                else:
                    cleaned_value = potential_json  # Handle nested JSON if needed
            except json.JSONDecodeError:
                # Fallback to regular stripping
                cleaned_value = value.strip()

            # Only store if not an empty string 
            if cleaned_value:
                cleaned_data[cleaned_key] = cleaned_value
            else:  # Optional: Store empty strings if needed 
                cleaned_data[cleaned_key] = ''

        elif isinstance(value, (list, dict)):  # Handle nested structures
            try:
                cleaned_value = json.dumps(value)  # Serialize for consistent string handling
                cleaned_data[cleaned_key] = cleaned_value
            except TypeError:
                raise ValueError(f"Cannot serialize value of type {type(value)} for key '{key}'")

        else:  
            cleaned_data[cleaned_key] = value  # Pass through non-string values

    return cleaned_data
