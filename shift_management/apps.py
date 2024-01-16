from django.apps import AppConfig


class ShiftManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shift_management'

    def ready(self):
            import shift_management.signals  # This imports your signals so they are ready to use