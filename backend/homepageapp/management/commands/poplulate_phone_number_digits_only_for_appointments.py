from django.core.management.base import BaseCommand
from appointments.models import AppointmentRequest
import re
import logging
from django.db import transaction
import time
import os

logger = logging.getLogger('django.management_script')
class Command(BaseCommand):
    help = 'Populate phone_number_digits_only field in PhonesNewSQL02Model'
    file_name = os.path.basename(__file__)

    def handle(self, *args, **kwargs):
        start_time = time.time()
        logger.info(f'Command {self.file_name} started at {start_time}...')
        try:
            with transaction.atomic():
                appointments = AppointmentRequest.objects.all()
                updated_appointments = []

                for appointment in appointments:
                    if appointment.appointment_phone_number:
                        phone_digits_only = re.sub(r'\D', '', appointment.appointment_phone_number)
                        appointment.appointment_phone_number_digits_only = phone_digits_only
                        updated_appointments.append(appointment)

                batch_size = 1000
                while updated_appointments:
                    batch = updated_appointments[:batch_size]
                    AppointmentRequest.objects.bulk_update(batch, ['appointment_phone_number_digits_only'])
                    updated_appointments = updated_appointments[batch_size:]

            elapsed_time = time.time() - start_time
            self.stdout.write(self.style.SUCCESS(
                'Successfully populated phone_number_digits_only field in {:.2f} seconds.'.format(elapsed_time)))
            logger.info('Command executed successfully in {:.2f} seconds'.format(elapsed_time))

        except Exception as e:
            logger.error('Error occurred: {}'.format(str(e)))
            self.stdout.write(self.style.ERROR('An error occurred.'))
