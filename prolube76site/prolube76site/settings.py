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

load_dotenv()  # take environment variables from .env.

#from .config.dev import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 
try:
    SECRET_KEY = os.getenv("DJANO_SECRET_KEY")
except KeyError as e:
    raise RuntimeError("Could not find a Django SECRET_KEY in the environment variables") from e


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ADMINS=[]

# ALLOWED_HOSTS=[]
ALLOWED_HOSTS = ["www.theironmanhouse.com","127.0.0.1","localhost",]

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'polls.apps.PollsConfig',
    'polls',
    'homepageapp',
    'appointments',
    'apis',  # adding the aps. 
    'internal_users',
    'dashboard',
    # 'firebase_auth', # google firebase-auth
]


# added on 2022-07-06 as an example customer settings for dev, staging or prod.
if os.environ.get('DJANGO._USE_DEBUG_TOOLBAR'):
    INSTALLED_APPS +=('debug_toolbar',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

WSGI_APPLICATION = 'prolube76site.wsgi.application'

# -- 2023-04-01 add a custom internal_users app to manage the future employees.
AUTH_USER_MODEL = 'internal_users.InternalUser'

# added so that when a user login from 127.0.0.1/users/login, he will be re-directed to 'dashboard/'.
# controlled by dashboard app. the main core app that do the lineitems and etc.
LOGIN_REDIRECT_URL = "/dashboard/"


# ----2023-04-03 add firebase auth package for external_users (customers) to use ---

## ENABLE this following script when firebase_admin is used across the site; especially when the external_users app (for customers)
# is created. 

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/2023-04-01-firebase-auth-private-key/fresh-start-9fdb6-firebase-adminsdk-yjbn6-92fef6fee6.json")
firebase_admin.initialize_app(cred)


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


### use the django-mssql-backend 

# DATABASES = {
#      'default': {
#          'ENGINE': 'mssql',
#          'NAME': 'ShopMgt',
#          'USER': 'SA',
#          'PASSWORD': '8189180941sS@',
#          'HOST': 'localhost',
#          'PORT': '1433',

#          'OPTIONS': {
#              'driver': 'ODBC Driver 18 for SQL Server',
#          },
#      },
#  } 

# DATABASES = {
#       'default': {
#           'ENGINE': 'django.db.backends.sqlite3',
#           'NAME': BASE_DIR / 'db.sqlite3',
#       }
#   }

 # 2022-07-04- hide sensitivie environemnt variables such as the database url and login info. 

if os.environ.get("DB_SERVER"):
    # load the environment variables
    server = os.getenv("DB_SERVER")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    databaseName = os.getenv("DB_DATABASE1")
# use the Microsoft provided MSSQL DRIVER for Django 
    DATABASES = {
          "default": {
              "ENGINE": "mssql",
              "NAME": databaseName,
              "USER": user,
              "PASSWORD":password,
              "HOST": server,
              "PORT": "",
              "OPTIONS": {"driver": 'ODBC Driver 18 for SQL Server', #  "ODBC Driver 18 for SQL Server", 
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



# 'django.db.backends.postgresql'
# 'django.db.backends.mysql'
# 'django.db.backends.sqlite3'
# 'django.db.backends.oracle'
    
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

STATIC_URL = 'static/'


# set up the base folder to host static files in 
# "76prolubeplus.com/prolube76site/static"
# static files include javacscript

# STATICFILES_DIRS = [
#     BASE_DIR / "static/bootstrap-5.0.2-dist/css",
#     BASE_DIR / "static/bootstrap-5.0.2-dist/js",
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

