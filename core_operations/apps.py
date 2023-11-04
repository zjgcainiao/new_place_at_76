from django.apps import AppConfig


class CoreOperationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_operations'

    def ready(self):
        import homepageapp.signals
