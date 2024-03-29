"""
Django settings for `automanshop `project. 

project updated: 2023-11-08

old project name: prolube76site

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from core_operations.utilities import test_db_connection  # Adjust the import based on your file structure
from google.oauth2 import service_account
import os
from dotenv import load_dotenv,  find_dotenv
from pathlib import Path
from decouple import config, Csv
import requests
import json
import firebase_admin
from firebase_admin import credentials
from core_operations.log_filters import LocalTimezoneFilter
import logging
from datetime import timedelta
import re
import ssl


# The find_dotenv() function will search for the .env file starting from the current working directory and then going up each parent directory until it finds one.
# So, even if your script isn't in the root of your project, find_dotenv() can still locate your .env file.
load_dotenv(find_dotenv())
# from .config.dev import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = config("DJANGO_SECRET_KEY")
except KeyError as e:
    raise RuntimeError(
        "Could not find a Django SECRET_KEY in the environment variables.") from e

# 'my_app_logs' directory is located at the base of my project
LOGGING_DIR = os.path.join(BASE_DIR, 'my_app_logs')
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'local_time': {
            '()': LocalTimezoneFilter,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
        },
        'request_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'requests.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
        },
        'db_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'db.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'security.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
        },
        'app_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'app.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
        },
        'external_api_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'external_api.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
        },

        'management_script_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'management_scripts.log'),
            'formatter': 'verbose',
            'filters': ['local_time'],
            'maxBytes': 5 * 1024 * 1024,  # Adjust size as needed
            'backupCount': 3,  # Adjust backup count as needed
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'request_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['console', 'db_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {  # Logger for customer_users and internal_users and all future user types
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'talent_management': {  # the name of your custom app `talent_management`
            'handlers': ['console', 'app_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'external_api': {  # Logger for external API interactions
            'handlers': ['console', 'external_api_file'],
            'level': 'INFO',
            'propagate': False,
        },

        'management_script': {  # Logger for management scripts
            'handlers': ['console', 'management_script_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logger = logging.getLogger("django")

# 2023-10-24 added OpenAI_API_key and OpenAI_API_key 2
OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_API_KEY2 = config("OPENAI_API_KEY2", default=OPENAI_API_KEY)
if OPENAI_API_KEY:
    logger.info("loading openai api key succesfully.")
else:
    logger.info("there is no openai api key found during Django server launch.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
DJANGO_PROD_ENV = config("DJANGO_PROD_ENV", default=True, cast=bool)
logger.info(
    f'Django debug has been set to {DEBUG}...Enable Production environment is {DJANGO_PROD_ENV}...')
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ORIGIN_WHITELIST
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:5173',  # Add the origin of your React app here
#     "http://localhost",
#     "http://127.0.0.1:8000",
#     "https://new76prolubeplus.com",
#     "https://storage.googleapis.com",
#     "https://automan-container-app.azurewebsites.net",
# ]

# Turn off CSRF secure in development env (HTTP); in production, HTTPS requires to have CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN", default="localhost")

if DEBUG:
    CSRF_COOKIE_SECURE = False
else:
    CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", default="new76prolubeplus.com", cast=Csv())

# ['new76prolubeplus.com', 'www.new76prolubeplus.com','76prolubeplus.azurewebsites.net']

# SECURE_SSL_REDIRECT = True

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ADMINS=[]


# 2023-10-17 added STRIPE two sets of keys.
# test keys.
STRIPE_PUBLIC_TEST_KEY = config("STRIPE_PUBLIC_TEST_KEY", default=None)
STRIPE_SECRET_TEST_KEY = config("STRIPE_SECRET_TEST_KEY", default=None)
# live keys. stripe
STRIPE_PUBLIC_LIVE_KEY = config("STRIPE_PUBLIC_LIVE_KEY", default=None)
STRIPE_SECRET_LIVE_KEY = config("STRIPE_SECRET_LIVE_KEY", default=None)

STRIPE_LIVE_SECRET_KEY = STRIPE_SECRET_LIVE_KEY
STRIPE_TEST_SECRET_KEY = STRIPE_SECRET_TEST_KEY

STRIPE_LIVE_MODE = False  # Change to True in production
STRIPE_WEBHOOK_TEST_SECRET = config("STRIPE_WEBHOOK_TEST_SECRET", default=None)
# DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
# DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
# DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id


# rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],


    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',  # default authentications
        'rest_framework.authentication.SessionAuthentication',  # default authentications
        # added to allow simpleJWTToken used between a React Native frontend and this application.
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ]
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# ALLOWED_HOSTS=[]
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    # "automanshop.apps.MyAdminConfig",
    'daphne',  # added for django-channel. # 2023-11-08
    'channels',  # added for django-channel. # 2023-11-08
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # allow sessions
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # humanize lib. so i can use to format phone numbers
    # 'polls.apps.PollsConfig',
    'corsheaders',
    'homepageapp',
    'appointments.apps.AppointmentsConfig',
    'django_recaptcha',
    'apis',  # adding the apis.
    'internal_users',
    'customer_users',
    'dashboard',
    'talent_management',
    'we_create_3d_models',
    'automatic_emails',
    'core_operations',
    'firebase_auth_app',
    'celery',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'captcha',  # google reCAPTCHA connection
    'formtools',
    'crispy_forms',  # add django-cripsy-form
    'crispy_forms_foundation',
    'crispy_bootstrap5',
    # 'social_django',
    # 'firebase_auth', # google firebase-auth
    'we_have_ai_helpers',
    'shift_management',
    'shops',
    # added on 2023-10-18. provding dtc trouble codes reading..
    'smart_diagnosis',
    # token authentication provied by Django Rest framework.
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'CRMs',  # CRMs app
    'we_handle_money_stuff',  # transactions, GL, accounting app
]
# in testing, add `django_sslserver2` to the installed apps.
if  DEBUG:
    INSTALLED_APPS += ('django_sslserver2',)

# added on 2022-07-06 as an example customer settings for dev, staging or prod.
# if os.environ.get('DJANGO._USE_DEBUG_TOOLBAR'):
#     INSTALLED_APPS +=('debug_toolbar',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    # added CorsMiddleWare from django-cors-headers
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom InternalUserMiddleware that applies to certain apps
    "internal_users.middlewares.InternalUserMiddleware",

    'core_operations.middlewares.ResponseTimeMiddleware',
    
    # custom middleware that limits the number of search requests
    # "core_operations.middlewares.SearchLimitMiddleware",
]

# if os.environ.get('DJANGO_USE_DEBUG_TOOLBAR'):
#     MIDDLEWARE += ('debug_toolbar.DebugToolMiddleware',)

ROOT_URLCONF = 'automanshop.urls'

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

# WSGI_APPLICATION = 'automanshop.wsgi.application'

# 2023-04-01 add a custom internal_users app to manage the future employees.
AUTH_USER_MODEL = 'internal_users.InternalUser'

AUTHENTICATION_BACKENDS = [
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


# added channel layer for the human operator's converation app (in CRMs app).
# 2023-11-08

# Use channels to manage ASGI
ASGI_APPLICATION = "automanshop.asgi.application"


# Use os.getenv to get environment variables
# 'REDIS_HOST' and 'REDIS_PORT' can be set to 'localhost' and '6379' respectively in your local .env file
# For production, set them to your Azure Redis Cache instance details
USE_LOCAL_REDIS = config("USE_LOCAL_REDIS", default=False, cast=bool)
# REDIS server dockerized flag, default to False
REIS_DOCKERIZED = config("REDIS_DOCKERIZED", default=False, cast=bool)
REIS_DOCKERIZED_HOST = config("REDIS_DOCKERIZED_HOST", default='localhost')

if not USE_LOCAL_REDIS:

    REDIS_HOST = config("LOCAL_REDIS_HOST", default=REIS_DOCKERIZED_HOST)
    # default to 6379 on local redis server (run `redis-server`)
    REDIS_PORT = config("LOCAL_REDIS_PORT", default=6379, cast=int)
    REDIS_PASSWORD = config('LOCAL_REDIS_PASSWORD', default=None)
    REDIS_USE_SSL = config('LOCAL_REDIS_USE_SSL', default=False, cast=bool)
    logger.info(f'using local redis server...{REDIS_HOST}...')
else:

    REDIS_HOST = config('REDIS_HOST', default=REIS_DOCKERIZED_HOST)
    REDIS_PORT = config('REDIS_PORT', default=6380, cast=int)
    REDIS_PASSWORD = config('REDIS_PASSWORD', default=None)
    REDIS_USE_SSL = config('REDIS_USE_SSL', default=False, cast=bool)
    logger.info(f'using redis server...{REDIS_HOST}...')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                ('rediss://:{password}@{host}:{port}'.format(
                    password=REDIS_PASSWORD,
                    host=REDIS_HOST,
                    ssl=True,
                    port=REDIS_PORT)
                 ),

            ],
            "channel_capacity": {
                "http.request": 200,
                "http.response!*": 10,
                re.compile(r"^websocket.send\!.+"): 20,
            }
        },
    },
}


# updated on 2023-11-17:
# reconfigured with Azure cache for redis instance. BACK IN USE!
# 2023-05-30
# Celery Configuration Options
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

CELERY_TIMEZONE = "America/Los_Angeles"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

# Celery broker settings for redis
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#conf-redis-result-backend
CELERY_BROKER_URL = [
    f'rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3?ssl_cert_reqs=required']
# Ensure secure Redis connection (SSL)
CELERY_BROKER_USE_SSL = {
    'ssl_cert_reqs': ssl.CERT_REQUIRED,
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# f'rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3?ssl_cert_reqs=required'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXPIRES = 3600  # 1 hour.

CELERY_RESULT_EXTENDED = True

# CELERY_RESULT_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL

# added so that when a user login from 127.0.0.1/users/login, he will be re-directed to 'dashboard/'.
# controlled by dashboard app. the main core app that do the lineitems and etc.
LOGIN_REDIRECT_URL = "/dashboard/"

# added on 2023-04-12 ---email
if os.environ.get('EMAIL_SENDER'):
    email_sender = os.environ.get('EMAIL_SENDER')
    email_pwd = os.environ.get('EMAIL_SENDER_PWD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # replace with your SMTP host
EMAIL_PORT = 587  # replace with your SMTP port. or 465
EMAIL_USE_TLS = True  # Use either TLS or SSL
EMAIL_USE_SSL = False
EMAIL_HOST_USER = email_sender  # replace with your email
EMAIL_HOST_PASSWORD = email_pwd  # replace with your email password
DEFAULT_FROM_EMAIL = email_sender  # replace with your email

# added on 2023-06-02 storage

# DEFAULT_FILE_STORAGE = 'myapp.custom_storage.NASStorage'
# NAS_STORAGE_LOCATION = '192.168.1.30'  # NAS server IP or hostname


# the google service account's credential json file stored online
google_credential_path = os.environ.get("GOOGLE_CREDENTIAL_PATH")

# Download the JSON file
response = requests.get(google_credential_path)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    credential_info = json.loads(response.text)

    # Use the JSON data to create the credentials object
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        credential_info)
    cred = credentials.Certificate(credential_info)
    logger.info(f'successfully downloaded the google sdk credential file (.json)')
else:
    logger.error(f"failing to download the google sdk credential file (.json)'")
    print("Failed to download the google sdk credential file (.json)")
    GS_CREDENTIALS = None
    cred = None

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# Replace with your Google Cloud Storage bucket name #2023_new_prolube76site/2023_talent_employment_docs
# '2023_new_prolube76site'  new name is vin-docor.appspot.com
GS_BUCKET_NAME = 'vin-doctor.appspot.com'  # 'vin-doctor.appspot.com'
GS_PROJECT_ID = 'vin-doctor'  # Replace with your Google Cloud project ID
GS_DEFAULT_ACL = 'publicRead'
GS_BUCKET_ACL = 'publicRead'
GS_AUTO_CREATE_BUCKET = True


# added 2024-01-11
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ----2023-04-03 add firebase auth package for external_users (customers) to use ---

# ENABLE this following script when firebase_admin is used across the site; especially when the external_users app (for customers)
# is created.

# initialize the firebase auth app.

default_app = firebase_admin.initialize_app(cred)
logger.info('initializing the firebase auth app in the django project...')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Add Google ReCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY")
if not RECAPTCHA_PRIVATE_KEY or not RECAPTCHA_PUBLIC_KEY:
    logger.error('missing google reCAPTCHA keys...')
RECAPTCHA_DOMAIN = 'www.recaptcha.net'

# ADD the following line for testing and local development
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']



# GOOGLE MAP API KEY FOR GOOGLE PLACES
GOOGLE_MAP_API_KEY = config("GOOGLE_MAP_API_KEY",default=None)

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# use the django-mssql-backend
# 2022-07-04- hide sensitivie environemnt variables such as the database url and login info.

local_server = config("DB_SERVER", default=False)
SQL_DOCKERIZED = config("SQL_DOCKERIZED", default=False, cast=bool)

if local_server and (not DJANGO_PROD_ENV):
    if SQL_DOCKERIZED:
        local_server = config("SQL_DOCKERIZED_HOST", default=None)
        logger.info(f'Using dockerized sql server {local_server}...')
    else:
        logger.info(f'Using local sql server:{local_server}...')

    # load the environment variables
    # user = config("DB_USER")
    try:
        user = config("DB_SA_USER")  # DB_APP_USER
        password = config("DB_SA_USER_PASSWORD")  # DB_APP_USER_PASSWORD
        databaseName = config("DB_DATABASE1")  # AutomanDB01
        demoDatabaseName = config("DEMO_DB_DATABASE_NAME")  # DemoDB01
    except FileNotFoundError as e:
        print(f"Error: The specified file was not found: {e}")
    except requests.exceptions.RequestException as e:
        print(
            f"Error: A network error occurred while attempting to download the credential file: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: The credential file could not be parsed as JSON: {e}")
    except (KeyError, ValueError) as e:
        print(
            f"Error: The credential file is missing required information: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        # handle the error here
        # print('using the DB_SERVER database')

    # use the Microsoft provided MSSQL DRIVER for Django
    DATABASES = {
        "default_actual": {
            "ENGINE": "mssql",
            "NAME": databaseName,
            "USER": user,
            "PASSWORD": password,
            "HOST": local_server,
            "PORT": "",
            "OPTIONS": {"driver": 'ODBC Driver 18 for SQL Server',  # "ODBC Driver 18 for SQL Server",
                        "extra_params": "TrustServerCertificate=yes;Encrypt=no;"
                        },
        },
        'default': {
            'ENGINE': 'mssql',
            "NAME": demoDatabaseName,
            "USER": user,
            "PASSWORD": password,
            "HOST": local_server,
            "PORT": "",
            "OPTIONS": {"driver": 'ODBC Driver 18 for SQL Server',  # "ODBC Driver 18 for SQL Server",
                        "extra_params": "TrustServerCertificate=yes;Encrypt=no;"
                        },
        }
    }
# when local_server is not available, use the Azure SQL DB.
else:
    logger.info('Using Azure SQL DB....')
    az_server = config("AZURE_DB_SERVER", default=False)
    az_user = config("AZURE_DB_USER")
    az_password = config("AZURE_DB_PASSWORD")
    az_databaseName = config("AZURE_DB_DATABASE")
    logger.info('the azure db server:database is: {}:{}...'.format(
        az_server, az_databaseName))

    # added on 2023-11-13

    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            "NAME": az_databaseName,
            "USER": az_user,
            "PASSWORD": az_password,
            "HOST": az_server,
            "PORT": "",
            "OPTIONS": {"driver": 'ODBC Driver 18 for SQL Server',  # "ODBC Driver 18 for SQL Server",
                        "extra_params": "TrustServerCertificate=yes;Encrypt=yes",
                        },
        },
    }

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

USE_I18N = True
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'  # 'UTC'

# turned the USE_TZ to False to avoid fetching data error when fetching data from the testing db.
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# STATIC_URL = 'static/'

# STATIC_URL = 'https://storage.googleapis.com/2023_new_prolube76site/static_files'

# STATIC_URL lin khttps://storage.googleapis.com/{}/static_files/'.format(GS_BUCKET_NAME) does not work when

# STATICFILES_STORAGE is set to 'storages.backends.gcloud.GoogleCloudStorage'

# https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string
# using azure storage bucket to host static files

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

STATIC_URL = 'https://storage.googleapis.com/{}/static_files/'.format(
    GS_BUCKET_NAME)

STATIC_ROOT = BASE_DIR / 'assets'


# STATIC_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'
# Azure Storage configurations
# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# AZURE_ACCOUNT_NAME = 'your_account_name'
# AZURE_ACCOUNT_KEY = 'your_account_key'  # You can use the connection string here
# AZURE_CONTAINER = 'your_container_name'
# AZURE_SSL = True  # Use https if True

# STATIC_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Test the database connection
# test_db_connection()
