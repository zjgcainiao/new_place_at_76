from django.apps import AppConfig


class CustomerUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_users'

    def ready(self):
        import customer_users.signals
