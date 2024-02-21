from django.utils import timezone
from datetime import datetime
def convert_date_to_yymmdd(date_string):
    # def convert_date_to_yymmdd(self, date_str):
    if not date_string:  # Handle empty strings
        return None

    date_formats = [
        '%m/%d/%y',  # e.g. "5/25/87"
        '%Y-%m-%d',  # e.g. "1987-05-25"
        '%d-%m-%Y',  # e.g. "25-05-1987"
        # ... you can add more popular date formats as needed
    ]

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_string, date_format)
            # Convert and return in desired format
            # return parsed_date.strftime('%Y-%m-%d')
            return timezone.make_aware(parsed_date)
        except ValueError:
            continue  # If this format fails, try the next one

    # If all parsing attempts fail, handle the unparsable date (e.g., return None or raise an error)
    return None  # Or you could raise a custom error if you want
