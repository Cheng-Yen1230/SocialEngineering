from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('Http_X_FORWARDED_PROTO', 'https')

