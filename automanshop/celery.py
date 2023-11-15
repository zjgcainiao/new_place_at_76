import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# similar to the setup in asgi.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automanshop.settings')

app = Celery('automanshop')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# We also add the Django settings module as a configuration source for Celery. This means that you don’t have to use multiple configuration files, and instead configure Celery directly from the Django settings; 
# but you can also separate them if wanted.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
