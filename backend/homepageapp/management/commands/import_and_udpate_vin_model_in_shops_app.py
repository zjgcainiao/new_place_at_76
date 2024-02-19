from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from homepageapp.models import VinNhtsaApiSnapshots
from shops.models import Vin

import time

class Command(BaseCommand):
    help = 'Populates or updates the Vin model with unique VINs from VinNhtsaApiSnapshots'

    def add_arguments(self, parser):
        # Optional argument to switch between create-only and update-if-exists modes
        parser.add_argument('--update', action='store_true', help='Update existing VIN records if they exist')

    def handle(self, *args, **options):
        start_time = time.time()
        unique_vins = VinNhtsaApiSnapshots.objects.values_list('vin', flat=True).distinct()

        try:
            with transaction.atomic():
                for vin_value in unique_vins:
                    if options['update']:
                        vin_obj, created = Vin.objects.update_or_create(vin=vin_value, defaults={'vin': vin_value})
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Created new VIN: {vin_value}'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'Updated existing VIN: {vin_value}'))
                    else:
                        # Create without updating existing ones
                        Vin.objects.get_or_create(vin=vin_value)

            self.stdout.write(self.style.SUCCESS(f'Successfully completed. Processed {len(unique_vins)} VIN(s).'))
        except Exception as e:
            raise CommandError(f'Error populating VINs: {e}')

        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(f'Completed in {end_time - start_time:.2f} seconds.'))
