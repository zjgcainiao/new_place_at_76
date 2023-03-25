#prolube76site/polls/dev.py

from .base import *
EMAIL_BACKEND='django.core.mail.backends.console.emailbackend'


# some variables are sensitive and shall be private
# added on 2022-07-06
MY_DB_HOST=''
MY_DB_DATABASE='default'
MY_DB_USER='stwang'
MY_DB_PASSWORD='sample-password'