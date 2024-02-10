import logging
from django.utils import timezone
from datetime import datetime


# class LocalTimezoneFilter(logging.Filter):
#     def filter(self, record):
#         record.local_time = timezone.localtime(record.created)
#         return True
class LocalTimezoneFilter(logging.Filter):
    def filter(self, record):
        # Convert the float to a naive datetime object
        naive_datetime = datetime.fromtimestamp(record.created)

        # Make the datetime object timezone aware using Django's default timezone
        aware_datetime = timezone.make_aware(naive_datetime)

        # Convert to local time
        record.local_time = timezone.localtime(aware_datetime)
        return True
