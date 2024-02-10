from django.core.management.base import BaseCommand
from homepageapp.models import PhonesNewSQL02Model
import re
import logging
from django.db import transaction
import time

logger = logging.getLogger('django.management_script')
class Command(BaseCommand):
    help = 'Populate phone_number_digits_only field in PhonesNewSQL02Model'

    def handle(self, *args, **kwargs):
        start_time = time.time()

        try:
            with transaction.atomic():
                phone_records = PhonesNewSQL02Model.objects.all()
                updated_phones = []

                for phone in phone_records:
                    if phone.phone_number:
                        phone_digits_only = re.sub(r'\D', '', phone.phone_number)
                        phone.phone_number_digits_only = phone_digits_only
                        updated_phones.append(phone)

                batch_size = 1000
                while updated_phones:
                    batch = updated_phones[:batch_size]
                    PhonesNewSQL02Model.objects.bulk_update(batch, ['phone_number_digits_only'])
                    updated_phones = updated_phones[batch_size:]

            elapsed_time = time.time() - start_time
            self.stdout.write(self.style.SUCCESS(
                'Successfully populated phone_number_digits_only field in {:.2f} seconds.'.format(elapsed_time)))
            logger.info('Command executed successfully in {:.2f} seconds'.format(elapsed_time))

        except Exception as e:
            logger.error('Error occurred: {}'.format(str(e)))
            self.stdout.write(self.style.ERROR('An error occurred.'))
