import os
import sys

import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔴 SECRET KEY (এনভায়রনমেন্ট ভ্যারিয়েবল থেকে নিবে, না থাকলে লোকালটি চলবে)
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-3d*d%e7_n3dga3aw99&evgb$d&jon)^fpjw9pgs%)*p%1hx%on"
)

# 🟢 কম্পিউটারে চললে DEBUG True, Render এ (RENDER env var থাকে) অটো False।
# চাইলে DJANGO_DEBUG=True/False দিয়ে override করা যাবে।
ON_RENDER = "RENDER" in os.environ
DEBUG = os.environ.get("DJANGO_DEBUG", str(not ON_RENDER)) == "True"

# 🟢 Allowed Hosts সেটআপ
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    # Render HTTPS proxy এর পেছনে চলে; এগুলো না থাকলে DEBUG=False এ login/POST এ CSRF 403 আসে
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # স্ট্যাটিক ফাইলের জন্য এটি দরকার
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# 🔵 Database Configuration (Step 14.5)
# হোস্টিং সার্ভারে DATABASE_URL থাকলে সেটি PostgreSQL ব্যবহার করবে, না থাকলে লোকালি SQLite চলবে
DATABASES = {
    "default": dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# 🟢 Static files Configuration (Step 14.4)
STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ডিয়াঙ্গোর নতুন সংস্করণের জন্য WhiteNoise স্টোরেজ কনফিগারেশন
# Manifest স্টোরেজ hashed ফাইলনাম (style.abc123.css) ব্যবহার করে এবং `collectstatic` আগে
# চালানো না থাকলে {% static %} এ "Missing staticfiles manifest entry" ValueError দেয়।
# `manage.py test` চলার সময় Django নিজে DEBUG=False করে দেয়, তাই টেস্টে সাধারণ স্টোরেজ ব্যবহার হয়।
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if TESTING
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# Email
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

# Auth Redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"
