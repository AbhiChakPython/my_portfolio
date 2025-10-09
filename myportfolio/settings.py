"""
Base Django settings for myportfolio project.
Designed for local development and base configuration, to be imported by settings_prod.py.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (for local testing only)
load_dotenv(BASE_DIR / '.env')

# ==============================================================================
# Django Core Settings - Local Defaults
# ==============================================================================

# SECURITY WARNING: Use a default key for local development.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-local-dev-key")

# DEBUG is TRUE in the base file. It MUST be explicitly set to False in settings_prod.py.
DEBUG = True

# Allowed hosts for local development. Production hosts are handled in settings_prod.py.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'base_app',
]

# 💡 CRITICAL FIX: Only include dev-only apps if DEBUG is True (i.e., local development).
if DEBUG:
    INSTALLED_APPS += [
        'django_browser_reload',
        'widget_tweaks',
    ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise is NOT used locally, only in production (in settings_prod.py)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 💡 CRITICAL FIX: Only include dev-only middleware if DEBUG is True (i.e., local development).
if DEBUG:
    MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware',
    ]


ROOT_URLCONF = 'myportfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myportfolio.wsgi.application'

# Database for local development (SQLite). Production config is in settings_prod.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation (default)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata") # Good practice to keep this configurable
USE_I18N = True
USE_TZ = True

# Static files for local development
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT and storage are handled in settings_prod.py

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
