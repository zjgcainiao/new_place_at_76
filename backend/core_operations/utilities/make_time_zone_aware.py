from .base import datetime, timezone

def make_timezone_aware(input_datetime, datetime_formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%f']):
    """
    Convert a naive datetime string or datetime object to a timezone-aware datetime object.

    Parameters:
    - input_datetime: The naive datetime string or datetime object.
    - datetime_formats: A list of datetime formats to try for parsing. Defaults to include common formats.

    Returns:
    - A timezone-aware datetime object or None.
    """
    if input_datetime is None:
        return None

    if isinstance(input_datetime, datetime):
        native_datetime = input_datetime
    elif isinstance(input_datetime, str):
        native_datetime = None
        for fmt in datetime_formats:
            try:
                native_datetime = datetime.strptime(input_datetime, fmt)
                break
            except ValueError:
                continue
        if native_datetime is None:
            return None
    else:
        raise TypeError(
            "The input must be either a datetime object or a string.")

    return timezone.make_aware(native_datetime)

