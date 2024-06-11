
import re

# common function 05
def capitalize_first_letters(string):

    # Check if the string is None or empty
    if not string:
        return ""

    # Use regex to split the string and handle extra spaces
    words = string.split()
    # words = re.split(r'(\s+)', string)  # This keeps the spaces in the result list

    # Capitalize the first letter of each segment if it contains any alphabetic character
    capitalized_words = [(word[0].upper() + word[1:] if word[0].isalpha() else word) for word in words if word]

    # Join the capitalized words back into a single string
    capitalized_string = ''.join(capitalized_words)

    return capitalized_string


