# main_app/context_processors.py
from django.conf import settings


def global_settings_for_homepageapp(request):
    # Return any necessary settings
    return {
        'VIN_DOCTOR_MODE_ON': settings.VIN_DOCTOR_MODE_ON,
    }
