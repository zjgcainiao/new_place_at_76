


def clean_string_in_dictionary_object(data):
    cleaned_data = {}
    for key, value in data.items():
        if key is None:
            raise ValueError("Encountered None as a dictionary key, which is unexpected.")
        
        # Convert to string in case the key is not a string type.
        key_str = str(key)
        
        # Remove the BOM from the beginning of the key if it's there
        cleaned_key = key_str.lstrip('\ufeff')
        
        if isinstance(value, str):
            cleaned_value = value.strip()
            cleaned_data[cleaned_key] = cleaned_value if cleaned_value else ''
        else:
            cleaned_data[cleaned_key] = value
    return cleaned_data