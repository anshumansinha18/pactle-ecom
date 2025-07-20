from .base import *
from config.env import get_current_env_value


SECRET_KEY = get_current_env_value("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_current_env_value('POSTGRES_DB'),
        'USER': get_current_env_value('POSTGRES_USER'),
        'PASSWORD': get_current_env_value('POSTGRES_PASSWORD'),
        'HOST': get_current_env_value('POSTGRES_HOST'),
        'PORT': get_current_env_value('POSTGRES_PORT'),
    }
}
