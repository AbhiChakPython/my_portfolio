import os
from pathlib import Path
from dotenv import load_dotenv

# ===============================
# Base Directory
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# Load Environment Variables (Dev Only)
# ===============================
if os.getenv("DJANGO_ENV", "dev").lower() == "dev":
    load_dotenv(BASE_DIR / ".env.dev")  # Load local dev env vars

# ===============================
# Core Settings
# ===============================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-local-dev-key")
DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")

# ===============================
# Installed Apps
# ===============================
INSTALLED_APPS = [
    # Default Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Apps
    'base_app',
]

# Dev-only apps
if DEBUG:
    INSTALLED_APPS += [
        'django_browser_reload',
        'widget_tweaks',
    ]

# ===============================
# Middleware
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware',
    ]

# ===============================
# URLs and WSGI
# ===============================
ROOT_URLCONF = 'myportfolio.urls'
WSGI_APPLICATION = 'myportfolio.wsgi.application'

# ===============================
# Templates
# ===============================
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

# ===============================
# Authentication
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ===============================
# Internationalization
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
USE_I18N = True
USE_TZ = True

# ===============================
# Static & Media
# ===============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===============================
# Default Primary Key
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===============================
# Database (will be overridden in dev/prod)
# ===============================
# This is a placeholder: actual DATABASES will be set in settings_dev.py or settings_prod.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ===============================
# Logging (optional base setup)
# ===============================
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True, parents=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[{asctime}] {levelname} {name}: {message}', 'style': '{'},
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_DIR / 'application.log',
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {'handlers': ['file'], 'level': 'WARNING'},
}