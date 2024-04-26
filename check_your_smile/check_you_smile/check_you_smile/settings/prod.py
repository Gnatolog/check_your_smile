from  .base import *
import os

DEBUG = False

ADMINS = [
    ('Robert','robertadamyanpy@gmail.com')
]

ALLOWED_HOSTS = ['checkyousmile.com','www.checkyousmile.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

RABBITMQ = {
    "PROTOCOL": "amqp", # in prod change with "amqps"
    "HOST": os.getenv("RABBITMQ_HOST", "rabbitmq"),
    "PORT": os.getenv("RABBITMQ_PORT", 5672),
    "USER": os.getenv("RABBITMQ_USER", "guest"),
    "PASSWORD": os.getenv("RABBITMQ_PASSWORD", "guest"),
}

CELERY_BROKER_URL = (f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:"
                     f"{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:"
                     f"{RABBITMQ['PORT']}")



