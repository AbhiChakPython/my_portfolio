"""
Django production settings for myportfolio project on Railway.
Overrides base settings with production-specific values.
"""
import os
import sys  # <--- CRITICAL: Import sys to check command-line arguments
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage

# Import all base settings (includes INSTALLED_APPS, MIDDLEWARE, TEMPLATES, BASE_DIR)
from .settings import * # noqa

# ==============================================================================
# Production Overrides
# ==============================================================================

# SECURITY WARNING: Use environment variable key, ensuring it's set
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not found in production!")

# Set DEBUG to False in production
DEBUG = False

# CRITICAL: Read ALLOWED_HOSTS from the environment variable provided by Railway.
allowed_hosts_str = os.getenv("ALLOWED_HOSTS")
if allowed_hosts_str:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.up.railway.app']

# ==============================================================================
# Database Configuration (Conditional Bypass for Collectstatic)
# ==============================================================================

# 🚨 CRITICAL FIX: Bypass the database check ONLY if we are running collectstatic.
# The Railway Build environment fails to resolve DATABASE_URL at this step.

if 'collectstatic' in sys.argv:
    # Use a dummy SQLite setup to satisfy Django's requirement to load settings.
    # This database will never actually be used.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db-dummy-build.sqlite3",
        }
    }
    print("INFO: Using dummy SQLite DB config for collectstatic command to complete build.")

else:
    # For all other commands (migrate, gunicorn), enforce the production DB connection.
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Use the full URL if available (preferred)
        DATABASES = {
            "default": dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
        print("INFO: Successfully configured PostgreSQL via DATABASE_URL.")
    else:
        # If DATABASE_URL is not found for a command that needs it, crash.
        raise ValueError(
            "CRITICAL: DATABASE_URL environment variable is missing for runtime command. "
            "Ensure the Postgres plugin is linked."
        )


# ==============================================================================
# Production Setup & Cleanup
# ==============================================================================

# Remove development-only apps/middleware imported from base settings
try:
    INSTALLED_APPS.remove('django_browser_reload')
except ValueError:
    pass
try:
    INSTALLED_APPS.remove('widget_tweaks')
except ValueError:
    pass
try:
    MIDDLEWARE.remove('django_browser_reload.middleware.BrowserReloadMiddleware')
except ValueError:
    pass

# Production Static Files (WhiteNoise setup)
# 1. Add WhiteNoise middleware for serving files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# 2. Define where collected static files will live
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 3. Use WhiteNoise storage backend for compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() in ["true", "1", "yes"]
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in ["true", "1", "yes"]
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() in ["true", "1", "yes"]
