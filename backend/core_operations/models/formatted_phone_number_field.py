from .base import models, US_COUNTRY_CODE, re

class FormattedPhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        kwargs['null'] = True
        kwargs['blank'] = True

        super().__init__(*args, **kwargs)

    def format_phone_number(self, phone_number):
        # phone_number = getattr(instance, self.attname)
        # Remove all non-digit characters from the phone number
        phone_number_digits = re.sub(r'\D', '', phone_number)

        # If the phone number is missing the country code, assume it's a US number
        if len(phone_number_digits) == 10:
            full_phone_number_digits = US_COUNTRY_CODE + phone_number_digits
            # Format the phone number as "+1 (818) 223-4456"
            return '+{}({}){}-{}'.format(
                full_phone_number_digits[0:1],
                full_phone_number_digits[1:4],
                full_phone_number_digits[4:7],
                full_phone_number_digits[7:11],
            )
        # 2023-05-22 when importing intital data into talent model from
        # 2023-05-01-talent_management_init.csv, the 1 is added.
        elif len(phone_number_digits) == 11:
            full_phone_number_digits = phone_number_digits
            return '+{}({}){}-{}'.format(
                full_phone_number_digits[0:1],
                full_phone_number_digits[1:4],
                full_phone_number_digits[4:7],
                full_phone_number_digits[7:11],
            )
        else:
            raise ValueError(
                'phone number must be 10 digits long. example: 234-456-3444 or (234)456-3444. The phone number entered is ', phone_number_digits)

    def pre_save(self, model_instance, add):
        phone_number = getattr(model_instance, self.attname)
        # model_instance.talent_phone_number_primary
        if phone_number:
            formatted_phone_number = self.format_phone_number(phone_number)
            setattr(model_instance, self.attname, formatted_phone_number)
            return formatted_phone_number
        return super().pre_save(model_instance, add)
