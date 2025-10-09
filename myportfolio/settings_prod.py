"""
Django production settings for myportfolio project on Railway.
*** THIS IS A TEMPORARY DIAGNOSTIC FILE. DO NOT KEEP IN FINAL CODE. ***
"""
import os
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage

# Import all base settings (including INSTALLED_APPS, MIDDLEWARE, TEMPLATES, BASE_DIR)
from .settings import *  # noqa


# Helper function for parsing environment variables (returns True/False)
def parse_bool_env(var_name, default_value):
    return os.getenv(var_name, str(default_value)).lower() in ['true', '1', 'yes']


# ==============================================================================
# >>> CRITICAL DEBUG STEP: PRINTING ENVIRONMENT VARIABLES <<<
# We must see what the environment variables are set to.
# ==============================================================================

print("\n\n!!! CRITICAL DATABASE DEBUG INFO START !!!")
# Print the raw values Python sees for the DATABASE_URL and the component PG variables
print(f"DATABASE_URL value: '{os.getenv('DATABASE_URL')}'")
print(f"PGHOST value: '{os.getenv('PGHOST')}'")
print(f"PGUSER value: '{os.getenv('PGUSER')}'")
print("!!! CRITICAL DATABASE DEBUG INFO END !!!\n")

# ==============================================================================
# Production Overrides
# The database logic below includes the robust checks, but if the variable is None,
# the print statement above will confirm it before the raise ValueError runs.
# ==============================================================================

# SECURITY WARNING: Use environment variable key, ensuring it's set
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not found in production!")

# Set DEBUG to False in production
DEBUG = False

allowed_hosts_str = os.getenv("ALLOWED_HOSTS")
if allowed_hosts_str:
    ALLOWED_HOSTS = [
        host.strip() for host in allowed_hosts_str.split(',') if host.strip()
    ]
else:
    ALLOWED_HOSTS = []

# ==============================================================================
# Database Configuration (Includes Fallback Check)
# ==============================================================================

# Check 1: Use the simple, resolved DATABASE_URL if available and not the interpolation string.
if os.getenv("DATABASE_URL") and os.getenv("DATABASE_URL") != '${{Postgres.DATABASE_URL}}':
    db_ssl_required = parse_bool_env('DB_SSL_REQUIRED', False)

    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=db_ssl_required
        )
    }
    print("INFO: Successfully configured database via resolved DATABASE_URL.")

# Check 2: Fallback to individual PG_* variables if DATABASE_URL is missing/unresolved
elif os.getenv("PGHOST") and os.getenv("PGUSER") and os.getenv("PGDATABASE"):
    print("WARNING: DATABASE_URL not found. Constructing from PG_* variables.")

    db_url = (
        f"postgres://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@"
        f"{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
    )

    db_ssl_required = parse_bool_env('DB_SSL_REQUIRED', False)

    DATABASES = {
        "default": dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=db_ssl_required,
        )
    }

# Check 3: Final failure if no variables are present
else:
    raise ValueError(
        "CRITICAL: Production environment variables for PostgreSQL are missing. "
        "Ensure the Postgres plugin is linked and the DATABASE_URL is injected."
    )

# ==============================================================================
# Static Files & Security (Copied from the final robust version)
# ==============================================================================

# Production Static Files (WhiteNoise setup)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = parse_bool_env('SECURE_SSL_REDIRECT', False)
SESSION_COOKIE_SECURE = parse_bool_env('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = parse_bool_env('CSRF_COOKIE_SECURE', False)
