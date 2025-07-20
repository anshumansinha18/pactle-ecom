#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from config.env import get_current_env_value


def main():
    """Run administrative tasks."""
    env = get_current_env_value("DJANGO_ENV")

    if env == "prod":
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.prod"
    elif env == "dev":
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.dev"
    else:
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.dev"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
