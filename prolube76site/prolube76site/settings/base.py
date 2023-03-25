"""
modified settings base file.
based on the original pro76lubesite.settings.py.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import Csv, config
from dotenv import load_dotenv


# from .config.dev import *

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# DO NOT EXPOSE SECRET_KEY in the settings.py file. store in the .env or other
# enviroment files.
try:
    SECRET_KEY = config('DJANGO_SECRET_KEY',
                        default="django-insecure$prolube76site.settings.local")
except KeyError as e:
    raise RuntimeError("Could not find a Django SECRET_KEY in the environment variables. check your .env or other .ini files") from e

# this following method requires a DJANGO_DEBUG defined in .env.
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

# SET UP THE ALLOWED HOSTS based on the dev/prod environments
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # the new library
    # 'django_pagination_bootstrap',
    # dd 'rest_framework' to your INSTALLED_APPS setting.
    'rest_framework',
    'django_rename_app',  # python manage.py rename_app <old_app_name> <new_app_name>
    # 'polls.apps.PollsConfig',
    'polls',
    'homepageapp',
    'appointments',
    'gunicorn',
]
# added on 2022-07-06 as an example customer settings for dev, staging or prod.
if os.environ.get('DJANGO_USE_DEBUG_TOOLBAR'):
    INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django_pagination_bootstrap.middleware.PaginationMiddleware',
]

if os.environ.get('DJANGO_USE_DEBUG_TOOLBAR'):
    MIDDLEWARE += ('debug_toolbar.DebugToolMiddleware',)

ROOT_URLCONF = 'prolube76site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI server -- gunicorn and etc.
WSGI_APPLICATION = 'prolube76site.wsgi.application'

# ==============================================================================
# DATABASES SETTINGS
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# ==============================================================================

# 2022-07-04- hide sensitivie environemnt variables such as the database url & login info.
# modified in November 2022.

if os.environ.get("DB_HOST"):
    # load the environment

    server = os.getenv("DB_SERVER")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    databaseName = os.getenv("DB_HOST")
# use the Microsoft provided MSSQL DRIVER for Django
    DATABASES = {
          "default": {
              "ENGINE": "mssql",
              "NAME": databaseName,
              "USER": user,
              "PASSWORD": password,
              "HOST": server,
              "PORT": "",
              "OPTIONS": {"driver": 'ODBC Driver 18 for SQL Server',  #  "ODBC Driver 18 for SQL Server",
              "extra_params": "TrustServerCertificate=yes;Encrypt=yes"
                          },
          },
      }
# use the django-pyodbc package
    # DATABASES = {
    # 'default': {
    #     'ENGINE': "django_pyodbc",
    #     'HOST':server,
    #     'USER': user,
    #     'PASSWORD': password,
    #     'NAME': databaseName,
    #     'OPTIONS': {
    #         'host_is_server': True
    #     },
    # }
    # }
else:
    DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }


# 'django.db.backends.postgresql'
# 'django.db.backends.mysql'
# 'django.db.backends.sqlite3'
# 'django.db.backends.oracle'

# use mysql database
    # DATABASES['default']={
    #      'ENGINE': 'django.db.backends.mysql',
    #      'HOST': os.environ.get('DB_HOST'),
    #      'NAME': os.environ.get('DB_DATABASE'),
    #      'USER': os.environ.get('MY_DB_USER'),
    #      'PASSWORD': os.environ.get('MY_DB_PASSWORD')
    #  }
# set this to False if you want to turn off pyodbc's connection pool
# DATABASE_CONNECTION_POOLING = False

# You can use a database backend that doesn’t ship with Django by setting ENGINE to a fully-qualified path (i.e. mypackage.backends.whatever).

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'  # 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'assets/'

# set up the base folder to host static files in
# "76prolubeplus.com/prolube76site/static"
# static files include javacscript

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / 'assets'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

# Note that how on the MEDIA_ROOT we are navigating two directories
# up to create a media directory outside the git repository but inside
# our project workspace (inside the directory simple/ (1)).
# So everything is handy and we won’t be committing test uploads to our repository

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR.parent.parent / "media"

# ==============================================================================
# FIRST-PARTY SETTINGS

# ==============================================================================

PROLUBE76SITE_ENVIRONMENT = config("PROLUBE76SITE_ENVIRONMENT", default="")

# `python -m pip install sentry_sdk` when needed
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# ==============================================================================
# SECURITY SETTINGS
# refer to the followind Django setting documentation
# https://docs.djangoproject.com/en/4.1/ref/settings/
# ==============================================================================
# Whether to use a secure cookie for the CSRF cookie.
# If this is set to True, the cookie will be marked as “secure”,
# which means browsers may ensure that the cookie is only sent with an HTTPS connection.


#The age of CSRF cookies, in seconds.
# CSRF_COOKIE_AGE = 60 * 60 * 24 * 7 * 52  # one year

# SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_SSL_REDIRECT = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1']

# ==============================================================================
# THIRD-PARTY APPS SETTINGS
# ==============================================================================
# sentry_sdk is a Error reporting/logging tool to catch exceptions raised in production
# sentry_sdk.init(
#     dsn=config("SENTRY_DSN", default=""),
#     environment=PROLUBE76SITE_ENVIRONMENT,
#     #release="prolube76site@%s" % prolube76site.__version__,
#     integrations=[DjangoIntegration()],
# )
