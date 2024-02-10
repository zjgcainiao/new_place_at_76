import os
import json
import csv
from datetime import datetime
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from decimal import Decimal, InvalidOperation
from django.utils import timezone

# Replace 'your_app' with your actual app name
from talent_management.models import TalentsModel as Talent


class Command(BaseCommand):
    help = 'Imports talents from a given CSV file'
    initial_data_filename = "2023-09-30-talent-management-dummy-data.csv"
    initial_data_filepath = "/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts"
    default_file_path = os.path.join(
        initial_data_filepath, initial_data_filename)

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help="The path to the CSV file to import.",
            nargs='?',  # This means the argument is optional
            # This sets the default value if the argument isn't provided
            default=self.default_file_path
        )

    def handle(self, *args, **kwargs):
        # file_path = options['file_path']
        file_path = kwargs.get('file_path', None)

        if not os.path.exists(file_path):
            raise CommandError(f"File '{file_path}' does not exist.")

        with open(file_path, 'r', encoding='utf-8-sig') as file:
            csv_data = csv.DictReader(file)
            # json_data = json.dumps([row for row in csv_data])
            data_list = [row for row in csv_data]
            talent_instances = []

            for aa in data_list:
                # Handle potential errors when processing a row
                try:
                    talent_instance, created = Talent.objects.update_or_create(
                        talent_id=aa['talent_id'],
                        defaults={
                            'talent_first_name': aa['talent_first_name'],
                            'talent_last_name': aa['talent_last_name'],
                            'talent_middle_name': aa['talent_middle_name'],
                            'talent_preferred_name': aa['talent_preferred_name'],
                            'talent_email': aa['talent_email'],
                            'talent_phone_number_primary': aa['talent_phone_number_primary'],
                            'talent_emergency_contact': aa['talent_emergency_contact'],
                            'talent_date_of_birth': self.convert_date_to_yymmdd(aa['talent_date_of_birth']),
                            'talent_physical_address_01': aa['talent_physical_address_01'],
                            'talent_physical_address_02': aa['talent_physical_address_02'],
                            'talent_physical_address_city': aa['talent_physical_address_city'],
                            'talent_physical_address_state': aa['talent_physical_address_state'],
                            'talent_physical_address_zip_code': aa['talent_physical_address_zip_code'],
                            'talent_physical_address_country': aa['talent_physical_address_country'],
                            'talent_mailing_address_is_the_same_physical_address': self.convert_to_boolean(aa[
                                'talent_mailing_address_is_the_same_physical_address']),
                            'talent_mailing_address_01': aa['talent_mailing_address_01'],
                            'talent_mailing_address_02': aa['talent_mailing_address_02'],
                            'talent_mailing_address_city': aa['talent_mailing_address_city'],
                            'talent_mailing_address_state': aa['talent_mailing_address_state'],
                            'talent_mailing_address_zip_code': aa['talent_mailing_address_zip_code'],
                            'talent_mailing_address_country': aa['talent_mailing_address_country'],
                            'talent_education_level': aa['talent_education_level'],
                            'talent_certifications': aa['talent_certifications'],
                            'talent_department': aa['talent_department'],
                            'talent_HR_remarks_json': aa['talent_HR_remarks_json'],
                            'talent_incident_record_json': aa['talent_incident_record_json'],
                            'talent_ssn': aa['talent_ssn'],
                            # 'talent_is_active': self.convert_to_boolean(aa['talent_is_active']) or False,
                            'talent_pay_type': self.convert_to_int(aa['talent_pay_type']) or 0,
                            'talent_pay_rate': self.convert_to_decimal(aa['talent_pay_rate']) or Decimal(0.0),
                            'talent_pay_frequency': self.convert_to_int(aa['talent_pay_frequency']) or 0,
                            'talent_previous_department': aa['talent_previous_department'],
                            # 'talent_years_of_work':aa['talent_years_of_work'],
                            'talent_supervisor_id': aa['talent_supervisor_id'],

                            'talent_hire_date': self.convert_date_to_yymmdd(aa['talent_hire_date']),
                            'talent_discharge_date': self.convert_date_to_yymmdd(aa['talent_discharge_date']),
                            # ... the rest of your fields
                        }
                    )
                    talent_instances.append(talent_instance)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(
                        f"Error processing row {aa}: {str(e)}"))
                    continue  # move to the next row

            # Use bulk_create to add all instances in a single query
            # with transaction.atomic():
            #     Talent.objects.bulk_create(
            #         talent_instances, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(
                f"Successfully imported {len(talent_instances)} talents."))

    @staticmethod
    def convert_date_to_yymmdd(date_string):
        # def convert_date_to_yymmdd(self, date_str):
        if not date_string:  # Handle empty strings
            return None

        date_formats = [
            '%m/%d/%y',  # e.g. "5/25/87"
            '%Y-%m-%d',  # e.g. "1987-05-25"
            '%d-%m-%Y',  # e.g. "25-05-1987"
            # ... you can add more popular date formats as needed
        ]

        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_string, date_format)
                # Convert and return in desired format
                # return parsed_date.strftime('%Y-%m-%d')
                return timezone.make_aware(parsed_date)
            except ValueError:
                continue  # If this format fails, try the next one

        # If all parsing attempts fail, handle the unparsable date (e.g., return None or raise an error)
        return None  # Or you could raise a custom error if you want

    @staticmethod
    def convert_to_int(value_str, default=None):
        # Convert a string to an integer. If it's empty or not valid, return the default value."""
        try:
            return int(value_str)
        except (ValueError, TypeError):  # This handles both empty strings and other invalid values
            return default

    @staticmethod
    def convert_to_decimal(value_str, default=None):
        # Convert a string to an integer. If it's empty or not valid, return the default value."""
        try:
            return Decimal(value_str)
        # This handles both empty strings and other invalid values
        except (ValueError, TypeError, InvalidOperation):
            return default

    @staticmethod
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
