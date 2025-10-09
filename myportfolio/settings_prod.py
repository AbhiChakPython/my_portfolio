"""
Django production settings for myportfolio project on Railway.
Overrides base settings with production-specific values.
"""
import os
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage

# Import all base settings (includes INSTALLED_APPS, MIDDLEWARE, TEMPLATES, BASE_DIR)
from .settings import * # noqa
# Note: E800 is ignored above because we are intentionally using wildcard import to override base settings.

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
# If ALLOWED_HOSTS is not set via environment variable, we default to the production URL structure.
allowed_hosts_str = os.getenv("ALLOWED_HOSTS")
if allowed_hosts_str:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
else:
    # Fallback to common Railway host pattern (replace with your actual domain if needed)
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.up.railway.app']

# ==============================================================================
# Database Configuration (Final, Confirmed Robust Structure)
# ==============================================================================

DATABASE_URL = os.getenv("DATABASE_URL")
DB_SSL_REQUIRED = os.getenv("DB_SSL_REQUIRED", "False").lower() in ["true", "1", "yes"]

if not DATABASE_URL:
    raise ValueError(
        "CRITICAL: DATABASE_URL environment variable is missing. "
        "Ensure the Postgres plugin is linked."
    )

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=DB_SSL_REQUIRED
    )
}
print("INFO: Successfully configured database via resolved DATABASE_URL.")


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
# Insert it right after SecurityMiddleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# 2. Define where collected static files will live
# NOTE: This overrides the 'staticfiles_dev' setting from the base file
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 3. Use WhiteNoise storage backend for compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings (aligned with your working deployment variables)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Read security settings from ENV variables, defaulting to 'False' as requested
# The lower()... checks handle "False", "false", "0" correctly.
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() in ["true", "1", "yes"]
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in ["true", "1", "yes"]
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() in ["true", "1", "yes"]
