# production environment setting.py
# created based on https://simpleisbetterthancomplex.com/tutorial/2021/06/27/how-to-start-a-production-ready-django-project.html


from .base import *

# in production, there should be NO DEBUGGING.


DEBUG = False

# ALLOWED_HOSTS = []


# The CSRF middleware and template tag provides easy-to-use protection against Cross Site Request Forgeries

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

# on the development, we explicitly disable the https connection due to an error received
# 2022-11-13
# SECURE_SSL_REDIRECT = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_SSL_REDIRECT = False
# SECURE_BROWSER_XSS_FILTER = False
# SECURE_CONTENT_TYPE_NOSNIFF = True