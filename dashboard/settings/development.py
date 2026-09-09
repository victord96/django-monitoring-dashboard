from .base import *

SECRET_KEY = os.getenv("IMI_SECRET_KEY")

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok.io",
    "http://127.0.0.1:8000",
]
INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES["default"].update(
    {
        "NAME": "CONFIDENTIAL",
        "USER": "CONFIDENTIAL",
        "PASSWORD": "CONFIDENTIAL",
        "HOST": "CONFIDENTIAL",
    }
)

INSTALLED_APPS.extend(["django_browser_reload"])
MIDDLEWARE.extend(["django_browser_reload.middleware.BrowserReloadMiddleware"])

try:
    from .local_settings import *
except ImportError:
    pass
