import json
import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from django.db import transaction
from django.core.management.base import BaseCommand
from homepageapp.models import VehiclesNewSQL02Model as Vehicle, VehicleNotesModel as VehicleNote


class Command(BaseCommand):
    help = 'popluate the VehicleNotesModel data with the original data source file in json'
    module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons'
    suffix_pattern = '_20230115.json'
    model_name = 'VehicleNotes'

    def handle(self, *args, **kwargs):
        logging.basicConfig(filename='vehiclenotes_logging_v01.log',
                            level=logging.ERROR)
        vehicle_dict = {
            vehicle_obj.vehicle_id: vehicle_obj for vehicle_obj in Vehicle.objects.all()}
        file_path = os.path.join(
            self.module_dir, self.model_name + self.suffix_pattern)
        with open(file_path, 'r') as f:
            data = json.load(f)
            # try:
            with transaction.atomic():  # wrap in a transaction
                errors = []  # intial error list. empty.
                for entry in data:

                    result = self.update_or_create_note(entry, vehicle_dict)
                    if result:
                        errors.append(result)
            if errors:
                self.stdout.write(self.style.ERROR('\n'.join(errors)))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'The VehicleNotesModel has been updated. Script run successfully.'))

    def update_or_create_note(self, entry, vehicle_dict):
        # if 'VehicleId' not in entry:
        #     error_msg = f"Skipping entry due to missing 'VehicleId': {entry}"
        #     logging.error(error_msg)
        #     return error_msg

        # Retrieve objects from stored dictionaries instead of DB queries
        vehicle_obj = vehicle_dict.get(entry.get('VehicleId'))

        # use update_or_create
        vehicle_note_data = {
            'vehicle': vehicle_obj,
            'vehicle_note_text': entry['NoteText'],
            'vehicle_note_type_id': entry['VehicleNoteTypeId'],
            'vehicle_note_last_updated_at': entry['LastChangeDate'],
        }
        try:
            vehicle_note_instance, created = VehicleNote.objects.create(
                **vehicle_note_data)
            # vehicle_note_instance.full_clean()
            # vehicle_note_instance.save()

        except Exception as e:
            error_msg = f"An error occurred while updating/creating a note for Vehicle with ID {entry['VehicleId']}: {e}"
            logging.error(error_msg)
            return error_msg
        return None
