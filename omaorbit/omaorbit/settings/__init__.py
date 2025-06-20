import os

# Default to development settings
environment = os.environ.get('DJANGO_ENV', 'dev')

if environment == 'prod':
    from .prod import *
else:
    from .dev import *
