


# common function 05
def capitalize_first_letters(string):
    # Split the string into individual words
    words = string.split()

    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]

    # Join the capitalized words back into a single string
    capitalized_string = ' '.join(capitalized_words)

    return capitalized_string


