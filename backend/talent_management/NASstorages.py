# 2023-06-02
# this file is not used. instead i setup the default_storage for the project to be the google cloud storage.
# SEE MORE IN THE `SETTINGS.PY`

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class NASStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        location = settings.NAS_STORAGE_LOCATION
        super().__init__(location, base_url)

    def get_available_name(self, name, max_length=None):
        # Generate a unique name by appending a number to the filename
        # This ensures that each employee's files are saved separately
        if self.exists(name):
            dir_name, file_name = os.path.split(name)
            root, ext = os.path.splitext(file_name)
            counter = 1
            while self.exists(name):
                name = os.path.join(dir_name, f"{root}_{counter}{ext}")
                counter += 1
        return name

    def get_employee_folder(self, employee_id):
        # Get the folder path for the employee based on their ID
        return os.path.join(self.location, f"talents_payroll_forms/employee_{employee_id}")

    def _save(self, name, content):
        employee_id = self.get_employee_id_from_name(name)
        folder = self.get_employee_folder(employee_id)
        return super()._save(os.path.join(folder, name), content)

    def get_employee_id_from_name(self, name):
        # Extract the employee ID from the filename
        filename = os.path.basename(name)
        employee_id, _ = os.path.splitext(filename)
        return employee_id
