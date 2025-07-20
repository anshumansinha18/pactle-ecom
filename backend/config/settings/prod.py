import os
import dj_database_url
from .base import *
from config.env import get_current_env_value, get_optional_env_value

SECRET_KEY = get_current_env_value("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

render_hostname = get_optional_env_value('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

database_url = get_optional_env_value('DATABASE_URL')
if database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
