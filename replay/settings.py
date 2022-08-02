from pathlib import Path
import dj_database_url
import os


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = not not os.getenv('DEBUG')
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap4',
    'replay.seo',
    'replay.theme',
    'replay.front',
    'replay.feeds',
    'replay.legal'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False
        }
    }
}

ROOT_URLCONF = 'replay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'replay.theme.context_processors.theme'
            ]
        }
    }
]

WSGI_APPLICATION = 'replay.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite')
    )
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

if not DEBUG:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'replay.'
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'  # NOQA
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'  # NOQA
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'  # NOQA
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'  # NOQA
    }
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = os.getenv('STATIC_URL') or '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT') or os.path.join(BASE_DIR, 'static')
MEDIA_URL = os.getenv('MEDIA_URL') or '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT') or os.path.join(BASE_DIR, 'media')

if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'  # NOQA

ANYMAIL = {
    'MAILGUN_API_KEY': os.getenv('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': 'out.origin.fm',
    'MAILGUN_API_URL': 'https://api.eu.mailgun.net/v3'
}

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = 'mark@out.origin.fm'

MARKDOWN_STYLES = {
    'default': {
        'extensions': (
            'markdown.extensions.smarty',
            'fenced_code'
        )
    },
    'legal': {
        'extensions': (
            'markdown.extensions.smarty',
            'markdown.extensions.toc'
        )
    }
}

MARKDOWNX_MARKDOWN_EXTENSIONS = MARKDOWN_STYLES['default']['extensions']
