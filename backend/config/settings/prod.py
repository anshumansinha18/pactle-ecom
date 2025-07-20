from .base import *
from config.env import get_current_env_value

SECRET_KEY = get_current_env_value("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
