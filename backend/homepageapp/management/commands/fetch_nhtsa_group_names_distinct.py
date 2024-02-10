# your_app/management/commands/remove_duplicates.py
from django.core.management.base import BaseCommand
from django.db.models.functions import Lower, Trim
from homepageapp.models import NhtsaVariableList


class Command(BaseCommand):
    help = 'Remove duplicates from variable_group_name in NhtsaVariableList'

    def handle(self, *args, **options):
        # Get the QuerySet with cleaned names
        queryset = (
            NhtsaVariableList.objects
            .exclude(variable_group_name__isnull=True)
            .annotate(
                cleaned_variable_group_name=Lower(Trim('variable_group_name'))
            )
            .values_list('cleaned_variable_group_name', flat=True)
        )

        # Fetch all values (no distinct yet) as a list
        all_names = list(queryset)

        # Create a set for case-insensitive comparison
        distinct_names_set = set()
        distinct_names_list = []

        for name in all_names:
            # This will handle case-insensitivity and spaces consistently
            cleaned_name = name.strip().lower()
            if cleaned_name not in distinct_names_set:
                distinct_names_set.add(cleaned_name)
                distinct_names_list.append(name)
        # distinct_names_list
        self.stdout.write(self.style.SUCCESS(
            f'Found {len(distinct_names_list)} distinct variable_group_names.'
        ))

        # Now you have a distinct list in distinct_names_list
        # Print it out in a format that's easy to copy into constants.py
        # self.stdout.write("\n".join(sorted(distinct_names_list)))

        # Optionally, print it out in a format ready to be pasted into a Python list
        self.stdout.write("POPULAR_NHTSA_GROUP_NAMES = [")
        self.stdout.write(",\n".join(
            f"    '{name}'" for name in sorted(distinct_names_list)))
        self.stdout.write("]")
        self.stdout.write(
            "copy this POPULAR_NHTSA_GROUP_NAMES and replace the one in consstans.py inside core_operations.constant.py.")
