from django.db import models
import re
import datetime
from django.utils import timezone
from django.db import models
from core_operations.constants import US_COUNTRY_CODE, NUMBER_OF_DAYS_IN_A_YEAR
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, CURRENT_TIME_SHOW_PRECISE_TIME_WITH_TIMEZONE, CURRENT_TIME_WITH_OUT_TIMEZONE
# constant value across the whole talent_managment app,

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

# custom field for the talent model.
# this custom field is not efficient, should be decommissioned soon. use @property instead.


class YearsOfWorkField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 5
        kwargs['decimal_places'] = 1
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def calculate_years_of_work(self, talent_hire_date):
        today = timezone.now().date()
        years = (today.days - talent_hire_date.days) / NUMBER_OF_DAYS_IN_A_YEAR

        return round(years, 1)

    def pre_save(self, model_instance, add):
        talent_hire_date = getattr(model_instance, self.attname)

        # when reading the initial data, the talent_hire_date could be empty string ''.
        # '%Y-%m-%d'
        if isinstance(talent_hire_date, str):
            if talent_hire_date:
                talent_hire_date = datetime.strptime(
                    talent_hire_date, '%Y-%m-%d')
            else:
                years_of_work = None
                return years_of_work
        if talent_hire_date:
            years_of_work = self.calculate_years_of_work(talent_hire_date)
            setattr(model_instance, self.attname, years_of_work)
            return years_of_work
        return super().pre_save(model_instance, add)



