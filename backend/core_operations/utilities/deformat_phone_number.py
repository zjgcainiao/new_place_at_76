


# common function 04
def deformat_phone_number(phone_number):
    # Remove non-digit characters from the phone number
    deformatted_number = ''.join(filter(str.isdigit, phone_number))

    return deformatted_number
