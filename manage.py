#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # --- Aligning settings module selection with working projects ---
    # Read DJANGO_ENV from the environment, defaulting to 'dev'.
    django_env = os.environ.get('DJANGO_ENV', 'dev').lower()

    if django_env == 'prod':
        # Load production settings for Railway deployment
        settings_module = 'myportfolio.settings_prod'
    else:
        # Load default settings for local development
        settings_module = 'myportfolio.settings'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    # --- End settings module selection ---

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