from django.apps import AppConfig


class TalentManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talent_management'

    def ready(self):
        import talent_management.signals
