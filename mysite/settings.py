"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
# SHERRIFF: Added import os here for the django_heroku fix at the bottom.
from pathlib import Path
import os
import sys
# print("DATABASE_URL:", os.environ.get('DATABASE_URL'))
try:
    import dj_database_url
except:
    1 + 1

# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ocydeh5ofpnwv4de&+1&3(d#&!8f6kz8(fdf&zjzbt^ditd=&7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SHERRIFF: Added both the local host and herokuapp.com here to handled the DisallowedHost error.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'medi-guard-cd00e1ea7845.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MediGuard',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_bootstrap5',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if 'ON_HEROKU' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'OPTIONS': {
            'TIME_ZONE': 'America/New_York'
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': '937163182869-595p36fa1ej0fnt5lgohur1i59vgt61d.apps.googleusercontent.com',
            'redirect_uris': ['http://127.0.0.1:8000//google/login/callback',
                              'https://medi-guard-cd00e1ea7845.herokuapp.com/accounts/google/login/callback/'],
            'key': '',
        },
        #         # only leave this in if not already a social account in admin
    }

}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# SHERRIFF: Added the static_root variable here to fix an error with static wd files not being found
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SHERRIFF
# Activate Django-Heroku.
# Use this code to avoid the psycopg2 / django-heroku error!
# Do NOT import django-heroku above!
try:
    if 'HEROKU' in os.environ:
        import django_heroku

        django_heroku.settings(locals())
except ImportError:
    found = False

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_LOGIN_ON_GET = True

AWS_STORAGE_BUCKET_NAME = "medi-giard"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Local
# STATICFILES_STORAGE = "storages.backends.s3.S3Storage"
# if not('ON_HEROKU' in os.environ):
#   import AWS_KEYS
#   AWS_ACCESS_KEY_ID = AWS_KEYS.AccessKey
#   AWS_SECRET_ACCESS_KEY = AWS_KEYS.SecretAccessKey
# AWS_QUERYSTRING_AUTH: False
# when push#
if not('ON_HEROKU' in os.environ):
    try:
        os.environ.get('AWS_ACCESS_KEY_ID')
        os.environ.get('AWS_SECRET_ACCESS_KEY')
    except:
        import AWS_KEYS
        AWS_ACCESS_KEY_ID = AWS_KEYS.AccessKey
        AWS_SECRET_ACCESS_KEY = AWS_KEYS.SecretAccessKey
AWS_QUERYSTRING_AUTH: False