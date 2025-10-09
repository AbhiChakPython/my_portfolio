"""
WSGI config for myportfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# The default is set here to ensure local runserver works without explicitly
# defining the variable. For production, the shell command (Procfile/Start Command)
# must override this before Gunicorn starts.
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
