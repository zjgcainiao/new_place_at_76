# from dateutil import parser
from .base import parser, logger

def pase_date_to_yymmdd(date_string):
    try:
        # Attempt to parse the date string automatically
        parsed_date = parser.parse(date_string)
        # Format the date as YYYY-MM-DD
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError as e:
        # Log an error if parsing fails
        logger.error(f"Failed to parse date with value '{date_string}'. Error: {e}")
        return date_string
