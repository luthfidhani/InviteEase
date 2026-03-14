import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "localhost").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "guests",
    "import_export",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "inviteease.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "inviteease.wsgi.application"

# Database: PostgreSQL if DATABASE_URL is set (Aiven, Supabase, …), else SQLite
_database_url = os.getenv("DATABASE_URL", "").strip()
if _database_url:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=_database_url,
            conn_max_age=600,
            ssl_require=True,
        )
    }
    # Supabase pooler / transaction mode: short-lived connections
    if ":6543" in _database_url or "pooler.supabase.com" in _database_url:
        DATABASES["default"]["CONN_MAX_AGE"] = 0

    # WSL2: DNS sering balikin IPv6 dulu; route IPv6 sering putus → "Network unreachable"
    # Pakai IPv4 literal sebagai HOST (gethostbyname = hanya record A)
    if os.getenv("DATABASE_FORCE_IPV4", "1") == "1":
        import socket
        from urllib.parse import urlparse

        hostname = DATABASES["default"].get("HOST") or urlparse(_database_url).hostname
        if hostname:
            try:
                ipv4 = socket.gethostbyname(hostname)
                DATABASES["default"]["HOST"] = ipv4
                opts = dict(DATABASES["default"].get("OPTIONS") or {})
                opts.setdefault("sslmode", "require")
                DATABASES["default"]["OPTIONS"] = opts
            except OSError:
                pass
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "data" / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth (login wajib untuk desk/dashboard; Screen tetap publik)
LOGIN_URL = "guests:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Channels
ASGI_APPLICATION = "inviteease.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
