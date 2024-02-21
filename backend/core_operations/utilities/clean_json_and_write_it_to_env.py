import json
from django.conf import settings
import os

def clean_json_and_write_to_env(json_string, env_var_key,filename=".env"):
    # Parse the JSON string to remove unnecessary whitespaces
    json_data = json.loads(json_string)
    cleaned_json_string = json.dumps(json_data, separators=(',', ':'))

    # Construct the full path to the .env file in the project root
    env_file_path = os.path.join(settings.BASE_DIR, filename)

    # Environment variable key
    env_var_key = env_var_key 
    env_content = f"\n{env_var_key}='{cleaned_json_string}'\n"

    # Write the cleaned JSON string to the .env file
    with open(env_file_path, 'a') as env_file:
        env_file.write(env_content)
    return cleaned_json_string


