from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'check_your_smile',
        'USER': 'admin_check',
        'PASSWORD': 'admin543check789po!',
        'HOST': 'localhost',
        'PORT': '',
    }
}

