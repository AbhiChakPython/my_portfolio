"""
Django production settings for myportfolio project on Railway.
Overrides base settings with production-specific values.
"""
import os
import dj_database_url

# Import all base settings
from .settings import * # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

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
# Database Configuration (Final Robust Check)
# ==============================================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Option 1: Use the full DATABASE_URL if available (preferred)
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    print("INFO: Using DATABASE_URL connection string.")

elif os.getenv("PGHOST") and os.getenv("PGUSER") and os.getenv("PGDATABASE"):
    # Option 2: Fallback to individual Railway-injected PG_* variables
    print("WARNING: DATABASE_URL not found. Constructing from PG_* variables.")

    # Construct the URL using the guaranteed PG variables
    db_url = (
        f"postgres://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@"
        f"{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
    )

    DATABASES = {
        "default": dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:
    # CRITICAL: If neither option works, raise an error to stop the deployment.
    raise ValueError(
        "CRITICAL: Production environment variables for PostgreSQL are missing. "
        "Ensure the Postgres plugin is linked and variables (DATABASE_URL or PG_*) are injected."
    )

# ==============================================================================
# Production Overrides
# ==============================================================================

# Remove development-only apps
INSTALLED_APPS.remove('django_browser_reload')
INSTALLED_APPS.remove('widget_tweaks')

# Remove development middleware
MIDDLEWARE.remove('django_browser_reload.middleware.BrowserReloadMiddleware')

# Production Static Files (WhiteNoise setup)
# 1. Add WhiteNoise middleware for serving files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# 2. Define where collected static files will live
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 3. Use WhiteNoise storage backend for compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings (Recommended for Production)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
