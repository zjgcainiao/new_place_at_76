  class AzureRouter:
    """
    A router to control all database operations on models in the
    myapp application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read myapp models go to azure_db.
        """
        if model._meta.app_label == 'myapp':
            return 'azure_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write myapp models go to azure_db.
        """
        if model._meta.app_label == 'myapp':
            return 'azure_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the myapp app is involved.
        """
        if obj1._meta.app_label == 'myapp' or \
           obj2._meta.app_label == 'myapp':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the myapp app only appears in the 'azure_db'
        database.
        """
        if app_label == 'myapp':
            return db == 'azure_db'
        return None