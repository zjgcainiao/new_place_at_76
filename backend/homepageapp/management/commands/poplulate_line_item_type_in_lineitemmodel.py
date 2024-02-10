from django.core.management.base import BaseCommand
from homepageapp.models import PartItemModel, LaborItemModel, NoteItemsNewSQL02Model,LineItemsNewSQL02Model,lineItemTaxesNewSQL02Model
import re
import logging
from django.db import transaction
import time

logger = logging.getLogger('django.management_script')
class Command(BaseCommand):
    help = "Updates the line_item_type field in the LineItemsNewSQL02Model."


    def handle(self, *args, **kwargs):
        start_time = time.time()
        batch_size = 100  # Define your desired batch size
        try:
            with transaction.atomic():
                line_items = LineItemsNewSQL02Model.objects.all()
                updated_items = []

                for line_item in line_items:
                    if PartItemModel.objects.filter(line_item=line_item).exists():
                        line_item_type = 'part'
                    elif LaborItemModel.objects.filter(line_item=line_item).exists():
                        line_item_type = 'labor'
                    elif NoteItemsNewSQL02Model.objects.filter(line_item=line_item).exists():
                        line_item_type = 'note'
                    else:
                        line_item_type = 'unknown'

                    line_item.line_item_type = line_item_type
                    updated_items.append(line_item)

                # Process in batches
                while updated_items:
                    batch = updated_items[:batch_size]
                    LineItemsNewSQL02Model.objects.bulk_update(batch, ['line_item_type'])
                    updated_items = updated_items[batch_size:]

            elapsed_time = time.time() - start_time
            self.stdout.write(self.style.SUCCESS(
                'Successfully updated line_item_type in {:.2f} seconds.'.format(elapsed_time)))
            logger.info('Command executed successfully in {:.2f} seconds'.format(elapsed_time))

        except Exception as e:
            logger.error('Error occurred: {}'.format(str(e)))
            self.stdout.write(self.style.ERROR('An error occurred.'))
