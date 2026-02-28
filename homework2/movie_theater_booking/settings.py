"""
Django settings for movie_theater_booking project.
Generated using Django 6.0.2
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------
# Security
# -------------------------

# Use environment variable in production (Render)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

# Default to False (safe). Set DEBUG=1 locally if needed.
DEBUG = os.environ.get("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "testserver",
    ".onrender.com",
    "app-mhagema3-21.devedu.io",
    "editor-mhagema3-21.devedu.io",
]

CSRF_TRUSTED_ORIGINS = [
    "https://app-mhagema3-21.devedu.io",
    "https://editor-mhagema3-21.devedu.io",
]


# -------------------------
# Applications
# -------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "bookings",
]


# -------------------------
# Middleware
# -------------------------

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


# -------------------------
# Templates
# -------------------------

ROOT_URLCONF = "movie_theater_booking.urls"

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

WSGI_APPLICATION = "movie_theater_booking.wsgi.application"


# -------------------------
# Database (SQLite for class)
# -------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# -------------------------
# Password validation
# -------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------
# Internationalization
# -------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------------
# Static files (Render)
# -------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -------------------------
# Login redirects
# -------------------------

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"