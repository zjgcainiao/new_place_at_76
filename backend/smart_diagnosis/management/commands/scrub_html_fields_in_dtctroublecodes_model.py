from django.core.management.base import BaseCommand
from django.db.models import F
from bs4 import BeautifulSoup
from smart_diagnosis.models import DtcTroubleCodes
from core_operations.custom_command import CustomCommand

# modified using customized command. core_operations.custom_command. comes with logger, time calculation and print out.


class Command(CustomCommand):
    help = 'Scrub HTML fields in the DtcTroubleCodes model to remove script tags and maintain proper formatting.'

    def handle(self, *args, **options):
        # getting the script_name based on the this sript
        self.set_script_name()

        # Query all the DtcTroubleCodes records.
        records = DtcTroubleCodes.objects.all()

        # Iterate over each record.
        for record in records:
            # Use introspection to loop through all the fields in the record.
            for field in record._meta.fields:
                # Check if the field name ends with "_html".
                if field.name.endswith("_html"):
                    field_value = getattr(record, field.name)
                    if field_value:
                        # Use BeautifulSoup to parse and clean the field value.
                        # Remember, using BeautifulSoup will remove the <script> tags but retain the proper formatting of the HTML. If you want to apply further checks or modifications to the HTML formatting, you can modify the BeautifulSoup parsing logic as needed.
                        soup = BeautifulSoup(field_value, 'html.parser')
                        # Remove all script tags.
                        [s.extract() for s in soup('script')]
                        # Set the cleaned HTML back to the field.
                        setattr(record, field.name, str(soup))
            record.save()
        self.done('Scrubbed HTML fields successfully in DtcTroubleCodes model!')
