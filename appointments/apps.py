from django.apps import AppConfig
import os


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    path = os.path.dirname(os.path.abspath(__file__))

    def ready(self):
        import appointments.signals
