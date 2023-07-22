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
                        default="django-insecure$prolube76site.setting_select.base")
except KeyError as e:
    raise RuntimeError("Could not find a Django SECRET_KEY in the environment variables. check your .env or other .ini files") from e

# this following method requires a DJANGO_DEBUG defined in .env.
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

# SET UP THE ALLOWED HOSTS based on the dev/prod environments
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    # "prolube76site.apps.MyAdminConfig",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # humanize lib. so i can use to format phone numbers

    # 'polls.apps.PollsConfig',
    'polls',
    
    'homepageapp',
    'appointments',
    'apis',  # adding the apis.
    'internal_users',
    'customer_users',
    'dashboard',
    'talent_management',
    'we_create_3d_models',
    'automatic_mails',
    'core_operations',
    'firebase_auth_app',

    'celery',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'captcha', # google reCAPTCHA connection
    'formtools',
    'crispy_forms', # add django-cripsy-form
    # 'crispy_bootstrap4',
    'crispy_bootstrap5',
    'social_django',
    # 'firebase_auth', # google firebase-auth
]
# added on 2022-07-06 as an example customer settings for dev, staging or prod.
# if DEBUG:
#     INSTALLED_APPS += ('debug_toolbar',)

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

# if DEBUG:
#     MIDDLEWARE += ('debug_toolbar.DebugToolMiddleware',)

# # Assume 'DJANGO_USE_DEBUG_TOOLBAR' is set to 'True' in development environment
# DJANGO_USE_DEBUG_TOOLBAR = config('DJANGO_USE_DEBUG_TOOLBAR', default=False, cast=bool)
# if DJANGO_USE_DEBUG_TOOLBAR:
#     DEBUG_TOOLBAR_CONFIG = {
#         'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG
#     }


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
# WSGI_APPLICATION = 'prolube76site.wsgi.application'

# 2023-04-01 add a custom internal_users app to manage the future employees.
AUTH_USER_MODEL = 'internal_users.InternalUser'

AUTHENTICATION_BACKENDS =[
                        # 'social_core.backends.open_id.OpenIdAuth',
                        # 'social_core.backends.google.GoogleOpenId',
                        # 'social_core.backends.google.GoogleOAuth2',
                        # 'social_core.backends.google.GoogleOAuth',
                        # 'social_core.backends.twitter.TwitterOAuth',
                        # 'social_core.backends.yahoo.YahooOpenId',  
                        "django.contrib.auth.backends.ModelBackend",
                        "internal_users.internal_user_auth_backend.InternalUserBackend",
                        "customer_users.customer_auth_backend.CustomerUserBackend",
                          ]

# 2023-05-30
# Celery Configuration Options
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

CELERY_TIMEZONE = "America/Los_Angeles"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Celery broker settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# added so that when a user login from 127.0.0.1/users/login, he will be re-directed to 'dashboard/'.
# controlled by dashboard app. the main core app that do the lineitems and etc.
LOGIN_REDIRECT_URL = "/dashboard/"


# added on 2023-04-12 ---email 
if config("EMAIL_SENDER"):
    email_sender = config('EMAIL_SENDER')
    email_pwd = config('EMAIL_SENDER_PWD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # replace with your SMTP host
EMAIL_PORT = 587 # replace with your SMTP port. or 465
EMAIL_USE_TLS = True # replace with your SMTP security settings
EMAIL_USE_SSL = False
EMAIL_HOST_USER = email_sender # replace with your email
EMAIL_HOST_PASSWORD = email_pwd # replace with your email password
DEFAULT_FROM_EMAIL = email_sender # replace with your email

# added on 2023-06-02 storage 

# DEFAULT_FILE_STORAGE = 'myapp.custom_storage.NASStorage'
# NAS_STORAGE_LOCATION = '192.168.1.30'  # NAS server IP or hostname

# # django < 4.2
# DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# # django >= 4.2
# STORAGES = {"default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"}}

# GS_BUCKET_NAME = 'YOUR_BUCKET_NAME_GOES_HERE'

# Configure Google Cloud Storage settings

# Import the required packages
# from storages.backends.gcloud import GoogleCloudStorage
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

from google.oauth2 import service_account

google_credential_path = os.environ.get("GOOGLE_CREDENTIAL_PATH")

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(google_credential_path)
GS_BUCKET_NAME = '2023_new_prolube76site'  # Replace with your Google Cloud Storage bucket name #2023_new_prolube76site/2023_talent_employment_docs
GS_PROJECT_ID = 'fresh-start-9fdb6'  # Replace with your Google Cloud project ID
GS_DEFAULT_ACL = 'publicRead'
GS_BUCKET_ACL = 'publicRead'
GS_AUTO_CREATE_BUCKET = True

# ----2023-04-03 add firebase auth package for external_users (customers) to use ---

## ENABLE this following script when firebase_admin is used across the site; especially when the external_users app (for customers)
# is created. 

import firebase_admin
from firebase_admin import credentials

# initialize the firebase auth app.
cred = credentials.Certificate(google_credential_path)
default_app = firebase_admin.initialize_app(cred)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Add Google ReCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
# ADD the following line for testing and local development
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# ==============================================================================
# DATABASES SETTINGS
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# ==============================================================================

# 2022-07-04- hide sensitivie environemnt variables such as the database url & login info.
# modified in November 2022.

server = config("DB_SERVER")
az_server = config("AZURE_DB_SERVER")
if config("DB_SERVER"):
# load the environment variables


    user = config("DB_USER")
    password = config("DB_PASSWORD")
    databaseName = config("DB_DATABASE1")

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
elif config(az_server):
    # azure db server

    az_user = config("AZURE_DB_USER")
    az_password = config("AZURE_DB_PASSWORD")
    az_databaseName = config("AZURE_DB_DATABASE")
    DATABASES = {
          "default": {
              "ENGINE": "mssql",
              "NAME": az_databaseName,
              "USER": az_user,
              "PASSWORD": az_password,
              "HOST": az_server,
              "PORT": "",
              "OPTIONS": {"driver": 'ODBC Driver 18 for SQL Server',  #  "ODBC Driver 18 for SQL Server",
              "extra_params": "TrustServerCertificate=yes;Encrypt=yes"
                          },
          },
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
    #  BASE_DIR / "static/bootstrap-5.0.2-dist/css",
    #  BASE_DIR / "static/bootstrap-5.0.2-dist/js",
]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
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
