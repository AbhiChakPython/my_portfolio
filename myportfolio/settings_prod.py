"""
Django production settings for myportfolio project on Railway.
Overrides base settings with production-specific values.
"""
import os
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage

# Import all base settings (including INSTALLED_APPS, MIDDLEWARE, TEMPLATES, BASE_DIR)
from .settings import * # noqa
# Note: E800 is ignored above because we are intentionally using wildcard import to override base settings.

# Helper function for parsing environment variables (returns True/False)
def parse_bool_env(var_name, default_value):
    return os.getenv(var_name, str(default_value)).lower() in ['true', '1', 'yes']


# ==============================================================================
# Production Overrides
# ==============================================================================

# SECURITY WARNING: Use environment variable key, ensuring it's set
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not found in production!")

# Set DEBUG to False in production
DEBUG = False

# CRITICAL: Read ALLOWED_HOSTS from the environment variable provided by Railway.
allowed_hosts_str = os.getenv("ALLOWED_HOSTS")
if allowed_hosts_str:
    # Ensure correct parsing from a comma-separated string
    ALLOWED_HOSTS = [
        host.strip() for host in allowed_hosts_str.split(',') if host.strip()
    ]
else:
    # Should not happen on Railway, but good safeguard
    ALLOWED_HOSTS = []

# ==============================================================================
# Database Configuration (FIXED & SSL Added)
# ==============================================================================

# Check for DATABASE_URL. If it is present and resolved, dj_database_url.config() will pick it up.
if os.getenv("DATABASE_URL"):
    # Fix 1: Read the DB_SSL_REQUIRED environment variable (defaults to False, matching your working project's environment).
    db_ssl_required = parse_bool_env('DB_SSL_REQUIRED', False)

    DATABASES = {
        "default": dj_database_url.config(
            # CRITICAL FIX: Omit the 'default' argument to let dj_database_url read the ENV var directly.
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=db_ssl_required # Fix 2: Explicitly set SSL requirement based on ENV
        )
    }
    print("INFO: Successfully configured database via resolved DATABASE_URL.")

# If the variable is missing, we raise a failure.
else:
    raise ValueError(
        "CRITICAL: Production environment variables for PostgreSQL are missing. "
        "Ensure the Postgres plugin is linked and the DATABASE_URL is injected."
    )


# ==============================================================================
# Production Setup
# ==============================================================================

# Remove development-only apps defined in base settings
try:
    INSTALLED_APPS.remove('django_browser_reload')
except ValueError:
    pass

try:
    INSTALLED_APPS.remove('widget_tweaks')
except ValueError:
    pass

# Remove development middleware defined in base settings
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

# Security settings (Now reading from environment, defaulting to False as per your request)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Read security variables from environment, defaulting to False to match your working deployment's setup.
SECURE_SSL_REDIRECT = parse_bool_env('SECURE_SSL_REDIRECT', False)
SESSION_COOKIE_SECURE = parse_bool_env('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = parse_bool_env('CSRF_COOKIE_SECURE', False)
