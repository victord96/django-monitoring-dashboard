from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Application name
APPLICATION_NAME = "IMI"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("IMI_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Host configuration
ALLOWED_HOSTS = []
CSRF_COOKIE_HTTPONLY = True


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "django_extensions",
    "active_link",
    # Local
    "core",
    "reports",
    "theme",
    "scorecard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URL configuration
ROOT_URLCONF = "dashboard.urls"
WSGI_APPLICATION = "dashboard.wsgi.application"
ASGI_APPLICATION = "dashboard.asgi.application"

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, "static")
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")


# Templates and assets
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR.parent, "templates"),
        ],
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

# assets
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [
    (
        os.path.join("fonts", "bootstrap-icons"),
        os.path.join(
            BASE_DIR.parent, "node_modules", "bootstrap-icons", "font", "fonts"
        ),
    )
]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("IMI_DB_NAME"),
        "USER": os.getenv("IMI_DB_USER"),
        "PASSWORD": os.getenv("IMI_DB_PASS"),
        "HOST": os.getenv("IMI_DB_HOST"),
        "PORT": 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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

# Authentication
AUTH_USER_MODEL = "core.User"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_URL


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ZABBIX_HOST = os.getenv("IMI_ZABBIX_HOST")
ZABBIX_API_KEY = os.getenv("IMI_ZABBIX_KEY")

if DEBUG:
    ZABBIX_INTEGRATION_CLASS = "scorecard.mock_zabbix_integration.MockZabbixIntegration"
else:
    ZABBIX_INTEGRATION_CLASS = "scorecard.zabbix_integration.ZabbixIntegration"
