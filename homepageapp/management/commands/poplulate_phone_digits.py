from django.core.management.base import BaseCommand
from homepageapp.models import PhonesNewSQL02Model
import re


class Command(BaseCommand):
    help = 'Populate phone_number_digits_only field in PhonesNewSQL02Model'

    def handle(self, *args, **kwargs):
        # Fetch all phone number records
        phone_records = PhonesNewSQL02Model.objects.all()

        for phone in phone_records:
            if phone.phone_number:
                # Remove all non-digit characters
                phone_digits_only = re.sub(r'\D', '', phone.phone_number)

                # Update the new field
                phone.phone_number_digits_only = phone_digits_only

                # Save the updated record
                phone.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated phone_number_digits_only field'))
