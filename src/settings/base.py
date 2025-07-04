"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import os
import os.path

from django.utils.translation import gettext_lazy as _

from decouple import config


###############################################################################
### BASIC SETTINGS                                                          ###
###############################################################################
DEBUG = config("DEBUG", default=False)

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",))

ENVIRONMENT = config("ENVIRONMENT", default="dev")

DJANGO_SETTINGS_MODULE = config("DJANGO_SETTINGS_MODULE", default="settings.dev")

ADMINS = (
    ("Artem Suvorov", "artem.suvorov@gmail.com"),
)
MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE":   config("DB_ENGINE", default="django.db.backends.sqlite3", cast=str),
        "NAME":     config("DB_NAME", default="sqlite.db", cast=str),
        "USER":     config("DB_USER", default="", cast=str),
        "PASSWORD": config("DB_PASSWORD", default="", cast=str),
        "HOST":     config("DB_HOST", default="", cast=str),
        "PORT":     config("DB_PORT", default="", cast=str),
        "OPTIONS": {
            # "autocommit": True,
        }
    }
}

DOMAIN_NAME = "example.com"
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = []
APPEND_SLASH = True

TIME_ZONE = "America/Los_Angeles"

LANGUAGE_CODE = "en-us"
LANGUAGES = (
    ("en",  _("English")),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "locale"),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

ADMIN_MEDIA_PREFIX = "/static/admin/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "staticserve")
STATICFILES_DIRS = (
    ("", f"{PROJECT_PATH}/static"),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

SECRET_KEY = config("SECRET_KEY", default="@zew8t_wcz!qn9=8+hheltx@&b#!x@i6ores96lhbnobr3jp*c")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)

print(f">>> {SECURE_SSL_REDIRECT=}")

TEMPLATES = [
    {
        "BACKEND":  "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_PATH, "templates/"),
            os.path.join(PROJECT_PATH, "templates/emails/"),
            os.path.join(PROJECT_PATH, "templates/cyborg/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug":    DEBUG,
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
            "context_processors": [
                "django.template.context_processors.csrf",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


###############################################################################
### DJANGO MIDDLEWARE CLASSES                                               ###
###############################################################################
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "urls"

WSGI_APPLICATION = "wsgi.application"

INSTALLED_APPS = (
    # --- Django Apps.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --- 3rd Party Apps.

    # --- Project Apps.
    "api",
    "app",
    "ecfr",
    # "tests",
)

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"


###############################################################################
### DJANGO CACHING                                                          ###
###############################################################################
CACHES = {
    "default": {
        "BACKEND":  "django.core.cache.backends.dummy.DummyCache",
    },
    "db": {
        "BACKEND":  "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "OPTIONS": {
            "MAX_ENTRIES":  1000,
        },
        "TIMEOUT":  60,
        "VERSION":  1,
    },
    "filebased": {
        "BACKEND":  "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
        "OPTIONS": {
            "MAX_ENTRIES":  1000,
        },
        "TIMEOUT":  60,
        "VERSION":  1,
    },
    "locmem": {
        "BACKEND":  "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "OPTIONS": {
            "MAX_ENTRIES":  1000,
        },
        "TIMEOUT":  60,
        "VERSION":  1,
    },
    "dummy": {
        "BACKEND":  "django.core.cache.backends.dummy.DummyCache",
    },
}


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################
LOGGING = {
    "version":                      1,
    "disable_existing_loggers":     False,
    "filters": {
        "require_debug_false": {
            "()":           "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()":           "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format":       "[{asctime}] {levelname} {message}",
            "datefmt":      "%Y-%m-%d %H:%M:%S",
            "style":        "{",
        },
        "verbose": {
            "format":       "[{asctime}] {levelname} [{name}.{funcName}:{lineno}] {message}",
            "datefmt":      "%Y-%m-%d %H:%M:%S",
            "style":        "{",
        },
    },
    "handlers": {
        "console": {
            "level":        "INFO",
            "filters": [
                "require_debug_true",
            ],
            "class":        "logging.StreamHandler",
            "formatter":    "verbose",  # "simple",
        },
        "plain_file": {
            "level":        "INFO",
            "class":        "logging.handlers.TimedRotatingFileHandler",
            "filename":     "logs/plain.log",
            "when":         "midnight",
            "interval":     1,
            "backupCount":  7,
            "formatter":    "verbose",
        },
        "null": {
            "class":        "logging.NullHandler",
        },
        "mail_admins": {
            "level":        "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class":        "django.utils.log.AdminEmailHandler",
            "formatter":    "verbose",
        },
    },
    "loggers": {
        "": {
            "level":        "INFO",
            "handlers":     ["console", "plain_file"],
            "propagate":    True,
        },
        "django": {
            "level":        "ERROR",
            "handlers":     ["console", "plain_file"],
            "propagate":    True,
        },
        "django.request": {
            "level":        "ERROR",
            "handlers":     ["console", "plain_file", "mail_admins"],
            "propagate":    True,
        },
        "py.warnings": {
            "handlers":     ["console", "plain_file"],
        },
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
# AUTH_USER_MODEL = "auth.User"


###############################################################################
### DJANGO REST FRAMEWORK                                                   ###
###############################################################################
INSTALLED_APPS += (
    "rest_framework",
    "rest_framework.authtoken",
)
REST_FRAMEWORK = {
    "DEFAULT_MODEL_SERIALIZER_CLASS":   "rest_framework.serializers.HyperlinkedModelSerializer",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
        # "rest_framework_jsonp.renderers.JSONPRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),

    "TEST_REQUEST_DEFAULT_FORMAT":  "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer"
    ),
}

