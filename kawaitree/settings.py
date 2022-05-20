"""
Django settings for kawaitree project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
from .env import ENV
import psycopg2.extensions
import os

if ENV == 'dev':
    print('Environnement de développement')
elif ENV == 'preprod':
    print('Environnement de préproduction')
else:
    print('Environnement de production')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['MYSECRETKEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ENV == 'dev':
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']

elif ENV == 'preprod':
    DEBUG = True
    ALLOWED_HOSTS = ['peter.nonsenz.lan', 'preprod.kawaitree.com']
    CSRF_TRUSTED_ORIGINS = ['https://preprod.kawaitree.com', 'http://peter.nonsenz.lan:81']
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

else:
    DEBUG = False
    ALLOWED_HOSTS = ['peter.nonsenz.lan', 'kawaitree.com']
    CSRF_TRUSTED_ORIGINS = ['https://kawaitree.com', 'http://peter.nonsenz.lan']
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

SITE_ID = 1
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/core'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'start',
    'users',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'crispy_bootstrap5',
    'vinaigrette',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'vinaigrette.middleware.VinaigretteAdminLanguageMiddleware',
]
SOCIALACCOUNT_PROVIDERS = {
   'google': {
      'SCOPE': [
         'profile',
         'email',
      ],
      'AUTH_PARAMS': {
         'access_type': 'online',
      }
   }
}
ROOT_URLCONF = 'kawaitree.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
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

WSGI_APPLICATION = 'kawaitree.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if ENV == 'dev':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif ENV == 'preprod':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'kawaitree-preprod',
            'USER': os.environ['KAWAIDBUSERPP'],
            'PASSWORD': os.environ['KAWAIDBPWPP'],
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'kawaitree',
            'USER': os.environ['KAWAIDBUSER'],
            'PASSWORD': os.environ['KAWAIDBPW'],
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en-us', _('English')),
    ('fr', _('French')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_FAIL_SILENTLY = not DEBUG

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# add this in the end of file
AUTHENTICATION_BACKENDS = (
   "django.contrib.auth.backends.ModelBackend",
   "allauth.account.auth_backends.AuthenticationBackend",
)
