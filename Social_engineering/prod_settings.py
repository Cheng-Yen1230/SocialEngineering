from .settings import *

STATIC_ROOT = 'staticfiles'
SECURE_PROXY_SSL_HEADER = ('Http_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = False
