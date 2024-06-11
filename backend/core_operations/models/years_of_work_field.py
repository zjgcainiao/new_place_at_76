# custom field for the talent model.
# this custom field is not efficient, should be decommissioned soon. use @property instead.
from .base import models, timezone, datetime, NUMBER_OF_DAYS_IN_A_YEAR, US_COUNTRY_CODE, re


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
