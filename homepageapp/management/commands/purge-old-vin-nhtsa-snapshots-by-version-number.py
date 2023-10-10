from django.core.management.base import BaseCommand
from homepageapp.models import VinNhtsaAPISnapshots
import logging

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = 'Purge old VIN snapshot records with version <= 0 in VinNhtsaAPISnapshots model.'

    def handle(self, *args, **kwargs):
        # Filter and delete the records
        deleted_records = VinNhtsaAPISnapshots.objects.filter(
            version__lte=0).delete()

        # Provide feedback on how many records were deleted
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {deleted_records[0]} old VIN snapshot records.'))
