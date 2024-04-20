"""
Django settings for control_server project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

def read_env(key, default):
    if key in os.environ:
        return os.environ[key]
    return default

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-be81ou_e=z4l_o=2x=@odz&ypvil&*$w5g%7wqte029i7pl2mr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

THIRD_PARY_APPS = [
    'rest_framework'
]
LOCAL_APPS = ['plant_control']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARY_APPS,
    *LOCAL_APPS
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

ROOT_URLCONF = "control_server.urls"

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

WSGI_APPLICATION = "control_server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

CAMERA_INDEX=0
SERVER_URL = read_env('SERVER_URL', 'localhost')
AUTHENTICATION_REQUIRED=True
USE_GPIO = read_env('USE_GPIO', 'TRUE') == 'TRUE'

GPIO_TIME_TO_WAIT = int(read_env('GPIO_TIME_TO_WAIT', '2'))
GPIO_USED_PIN = int(read_env('GPIO_USED_PIN', '16'))

#Only used if USE_GPIO = False
ARDUINO_PORT = read_env('ARDUINO_PORT', '/dev/ttyACM0')
ARDUINO_BAUDRATE = 9600
PUMP_ACTIVATION_CHAR = 'A'


BASE_PROTOCOL = 'http'
if 'https' in SERVER_URL:
    BASE_PROTOCOL = 'https'

OWN_IP = read_env('OWN_IP', '')
SERVER_URL = SERVER_URL.strip().replace('http://', '').replace('https://', '')
OWN_IP = OWN_IP.strip().replace('http://', '').replace('https://', '')

ALLOWED_HOSTS = ['localhost', OWN_IP, SERVER_URL]
print('ALLOWED_HOSTS', ALLOWED_HOSTS)
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', '%s://%s:8000' % (BASE_PROTOCOL, SERVER_URL),
'http://%s:8000' % OWN_IP]
print('CSRF_TRUSTED_ORIGINS', CSRF_TRUSTED_ORIGINS)

