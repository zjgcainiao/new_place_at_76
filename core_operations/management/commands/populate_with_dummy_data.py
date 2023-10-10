from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
# Import the function you've defined earlier
from core_operations.common_functions import update_with_dummy_data
import logging
from django.utils import timezone

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = 'Populate the database with dummy data.'
    logger.info("Starting the management command...")
    logger.info(
        f"{timezone.now()} preparing to run the script that update models in certain app with dummy data. 2023 Sept version. Apps:[appointments', 'homepageapp', 'dashboard']")

    def handle(self, *args, **options):
        apps_to_update = ['appointments', 'homepageapp', 'dashboard']

        for app_name in apps_to_update:
            try:
                app_config = apps.get_app_config(app_name)
            except LookupError:
                logger.error(f"App {app_name} does not exist.")
                raise CommandError(f"App '{app_name}' doesn't exist.")
            try:
                # Iterate through each model in the app
                for model in app_config.get_models():
                    logger.info(
                        f"Started updating model {model.__name__} in app {app_name}.")
                    self.stdout.write(
                        f"Updating model {model.__name__} in app {app_name}...")
                    updated_records = update_with_dummy_data(
                        model, 'default')  # Call the function
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully updated {updated_records} records in model {model.__name__}"))

            except Exception as e:
                logger.error(f"error while updating: {str(e)}")

        self.stdout.write(self.style.SUCCESS(
            'Finished updating all specified models with dummy data.'))
        logger.info("Finished updating all specified models with dummy data.")
