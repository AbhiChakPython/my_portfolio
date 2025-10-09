from .settings import *  # Import all base settings
import dj_database_url
import os

# ===============================
# Production Core Settings
# ===============================
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not found in production!")

DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]

# ALLOWED_HOSTS from Railway environment variable
allowed_hosts_str = os.getenv("ALLOWED_HOSTS")
if allowed_hosts_str:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.up.railway.app']

# ===============================
# Database (PostgreSQL via DATABASE_URL)
# ===============================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", 600)),
            ssl_require=os.getenv("DB_SSL_REQUIRED", "True").lower() in ["true", "1", "yes"],
            conn_health_checks=True,
        )
    }
else:
    # Fallback SQLite for dummy build (rarely used in prod)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db-dummy-build.sqlite3",
        }
    }

# ===============================
# Remove dev-only apps/middleware
# ===============================
for app in ['django_browser_reload', 'widget_tweaks']:
    if app in INSTALLED_APPS:
        INSTALLED_APPS.remove(app)

if 'django_browser_reload.middleware.BrowserReloadMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('django_browser_reload.middleware.BrowserReloadMiddleware')

# ===============================
# Whitenoise for static files
# ===============================
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ===============================
# Security Settings
# ===============================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() in ["true", "1", "yes"]
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True").lower() in ["true", "1", "yes"]
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True").lower() in ["true", "1", "yes"]

# ===============================
# Static & Media
# ===============================
# STATIC_ROOT already set above for Whitenoise
MEDIA_ROOT = BASE_DIR / 'media'

# ===============================
# Optional: Logging (production-ready)
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

# ===============================
# Third-party services (example)
# ===============================
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")