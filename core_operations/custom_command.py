# custom_command.py

import time
import logging
from django.core.management.base import BaseCommand
import os


class CustomCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('management_script')
        self.start_time = time.time()

    # create set_script_name() and the child calls it like self.set_script_name()
    def set_script_name(self):
        # Get the base name of the inheriting script
        self.script_name = os.path.basename(self.__module__)
        self.logger.info(f'starting management script {self.script_name}...')
        print(f'starting management script {self.script_name}...')

    def done(self, msg=None):
        if not msg:
            msg = f'Script {self.script_name} runs successfully.'
        elapsed_time = time.time() - self.start_time
        self.logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        print(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        self.stdout.write(self.style.SUCCESS(msg))
