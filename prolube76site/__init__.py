from django import get_version

VERSION = (1, 0, 0, "final", 0)

__version__ = get_version(VERSION)


from .celery import app as celery_app
__all__ = ('celery_app',)

