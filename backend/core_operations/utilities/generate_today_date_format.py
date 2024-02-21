from .base import timezone
# common function 02
def generate_today_date_format():
    # Get the current timezone setting
    timezone_setting = timezone.get_current_timezone()

    # Get the current date and time in the specified timezone
    current_datetime = timezone.now().astimezone(timezone_setting)

    # Generate the today's date formatted as 'YYYY_MM_DD_'
    today_date = current_datetime.strftime('%Y_%m_%d_')

    # Generate the full datetime formatted as 'YYYY_MM_DD_HH_MMMM'
    today_full_datetime = current_datetime.strftime('%Y_%m_%d_%H_%M')

    return today_date, today_full_datetime

