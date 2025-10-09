#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # Use settings_prod if DJANGO_SETTINGS_MODULE is set, otherwise default to local settings
    default_settings = 'myportfolio.settings'

    if os.getenv('DJANGO_ENV') == 'production':
        default_settings = 'myportfolio.settings_prod'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)

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
