from .base import *

DEBUG = True

# ALLOWED_HOSTS = []

# on the development, we explicitly disable the https connection due to an error received
# 2022-11-13
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = True