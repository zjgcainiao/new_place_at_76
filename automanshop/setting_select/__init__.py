# from decouple import config

# # In the .env file, there should  be flagging constant named "DJANGO_PROD_ENV"; the field flags if 
# # the running environment is Production (.prod import *) or DEVELOPMENT
# # other tests.py, local.py have not been used yet. 
# # 2022-11-13


# if config("DJANGO_PROD_ENV", default=True, cast=bool):
#     from .prod import *
# else:
#     from .dev import *
