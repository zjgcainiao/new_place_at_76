"""
Django settings for prolube76site project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from decouple import config, Csv
import requests
import json
import firebase_admin
from firebase_admin import credentials

load_dotenv()  # take environment variables from .env.

# from .config.dev import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 
try:
    SECRET_KEY = os.getenv("DJANO_SECRET_KEY")
except KeyError as e:
    raise RuntimeError("Could not find a Django SECRET_KEY in the environment variables.") from e


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

# ADMINS=[]

# ALLOWED_HOSTS=[]
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())
# ALLOWED_HOSTS = ["new76prolubeplus.azurewebsites.net", "new76prolubeplus.com",
#                  "127.0.0.1","localhost","192.168.1.83",]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    # "prolube76site.apps.MyAdminConfig",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # humanize lib. so i can use to format phone numbers

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
    # 'social_django',
    # 'firebase_auth', # google firebase-auth
]


# added on 2022-07-06 as an example customer settings for dev, staging or prod.
# if os.environ.get('DJANGO._USE_DEBUG_TOOLBAR'):
#     INSTALLED_APPS +=('debug_toolbar',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# if os.environ.get('DJANGO_USE_DEBUG_TOOLBAR'):
#     MIDDLEWARE += ('debug_toolbar.DebugToolMiddleware',)

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

WSGI_APPLICATION = 'prolube76site.wsgi.application'


# 2023-04-01 add a custom internal_users app to manage the future employees.
AUTH_USER_MODEL = 'internal_users.InternalUser'

AUTHENTICATION_BACKENDS =[
                        'social_core.backends.open_id.OpenIdAuth',
                        'social_core.backends.google.GoogleOpenId',
                        'social_core.backends.google.GoogleOAuth2',
                        'social_core.backends.google.GoogleOAuth',
                        'social_core.backends.twitter.TwitterOAuth',
                        'social_core.backends.yahoo.YahooOpenId',  
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
    email_sender = os.environ.get('EMAIL_SENDER')
    email_pwd = os.environ.get('EMAIL_SENDER_PWD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # replace with your SMTP host
EMAIL_PORT = 587 # replace with your SMTP port. or 465
EMAIL_USE_TLS = True # replace with your SMTP security settings
EMAIL_USE_SSL = False
EMAIL_HOST_USER = email_sender # replace with your email
EMAIL_HOST_PASSWORD = email_pwd # replace with your email password
DEFAULT_FROM_EMAIL = email_sender # replace with your email

# added on 2023-06-02 storage 

DEFAULT_FILE_STORAGE = 'myapp.custom_storage.NASStorage'
NAS_STORAGE_LOCATION = '192.168.1.30'  # NAS server IP or hostname

# # django < 4.2
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# # django >= 4.2
# STORAGES = {"default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"}}

# GS_BUCKET_NAME = 'YOUR_BUCKET_NAME_GOES_HERE'

# Configure Google Cloud Storage settings

# Import the required packages
# from storages.backends.gcloud import GoogleCloudStorage
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

from google.oauth2 import service_account

google_credential_path = os.environ.get("GOOGLE_CREDENTIAL_PATH")

# Download the JSON file
response = requests.get(google_credential_path)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    credential_info = json.loads(response.text)

    # Use the JSON data to create the credentials object
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(credential_info)
    cred = credentials.Certificate(credential_info)
else:
    print("Failed to download the google sdk credential file (.json)")
    GS_CREDENTIALS = None
    cred = None

GS_BUCKET_NAME = '2023_new_prolube76site'  # Replace with your Google Cloud Storage bucket name #2023_new_prolube76site/2023_talent_employment_docs
GS_PROJECT_ID = 'fresh-start-9fdb6'  # Replace with your Google Cloud project ID
GS_DEFAULT_ACL = 'publicRead'
GS_BUCKET_ACL = 'publicRead'
GS_AUTO_CREATE_BUCKET = True

# ----2023-04-03 add firebase auth package for external_users (customers) to use ---

## ENABLE this following script when firebase_admin is used across the site; especially when the external_users app (for customers)
# is created. 



# initialize the firebase auth app.

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


### use the django-mssql-backend 

 # 2022-07-04- hide sensitivie environemnt variables such as the database url and login info. 

if config("DB_SERVER"):
# load the environment variables

    server = os.environ.get("DB_SERVER")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    databaseName = os.environ.get("DB_DATABASE1")

    # azure db server
    az_server = os.environ.get("AZURE_DB_SERVER")
    az_user = os.environ.get("AZURE_DB_USER")
    az_password = os.environ.get("AZURE_DB_PASSWORD")
    az_databaseName = os.environ.get("AZURE_DB_DATABASE")
    # use the Microsoft provided MSSQL DRIVER for Django 
    DATABASES = {
            #
            "default": {
                "ENGINE": "mssql",
                "NAME": az_databaseName,
                "USER": az_user,
                "PASSWORD": az_password,
                "HOST": az_server,
                "PORT": "",
                "OPTIONS": {
                    "driver": 'ODBC Driver 18 for SQL Server',
                    "extra_params": "TrustServerCertificate=yes;Encrypt=yes;"
                },
            },
            # az db server is set to the default 2023-07-08
            "azure_db": {
                "ENGINE": "mssql",
                "NAME": az_databaseName,
                "USER": az_user,
                "PASSWORD": az_password,
                "HOST": az_server,
                "PORT": "",
                "OPTIONS": {
                    "driver": 'ODBC Driver 18 for SQL Server', 
                    "extra_params": "TrustServerCertificate=yes;Encrypt=yes;"
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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

USE_I18N = True
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles' #'UTC'

USE_TZ = False # turned the USE_TZ to False to avoid fetching data error when fetching data from the testing db.

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# STATIC_URL = 'static/'

# STATIC_URL = 'https://storage.googleapis.com/2023_new_prolube76site/static_files'

# STATIC_URL = 'https://storage.googleapis.com/{}/static_files/'.format(GS_BUCKET_NAME)

# this setup won't work with bucket's subfolder when staticfiles_storage is default to googlecloudstorage

STATIC_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)

STATIC_ROOT = BASE_DIR / 'assets'

# using storage bucket to host static files

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

