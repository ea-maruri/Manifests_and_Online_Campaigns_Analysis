"""
Django settings for Manifests_and_Online_Campaigns_Analysis project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5u6@nc35cq!u&nd&-=d$dv6zyzk3&pka+l2^m1c^zcd=^2*5bp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['xterm.mynetgear.com', '186.101.140.163',
                 '127.0.0.1', 'localhost', '0.0.0.0', '192.168.1.14', '192.168.200.8']

SECURE_SSL_REDIRECT = False  # Variable for SSL

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'djangosecure',  # allows https
    # 'sslserver', # for checking ssl
    # 'bootstrap_modal_forms',
    'StudyCasesManage',  # my app
    'StudyCasesConfApp',  # my app
]

MIDDLEWARE = [
    # 'djangosecure.middleware.SecurityMiddleware',  # For HTTPS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Manifests_and_Online_Campaigns_Analysis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Manifests_and_Online_Campaigns_Analysis/templates',
                 BASE_DIR / 'StudyCasesManage/templates/StudyCasesManage',
                 BASE_DIR / 'StudyCasesConfApp/templates/StudyCasesConfApp'],
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

WSGI_APPLICATION = 'Manifests_and_Online_Campaigns_Analysis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'studycases',
        'USER': 'postgres',
        'PASSWORD': 'Ecuador12',
        'HOST': 'localhost,',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
# if not DEBUG:
#     # STATIC_ROOT = ''
#     STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'Manifests_and_Online_Campaigns_Analysis', 'static'),
    #     BASE_DIR / 'static',
)


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Mailing
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587 # port for TLS in gmail
EMAIL_HOST_USER = 'ea.maruri@gmail.com'
EMAIL_HOST_PASSWORD = '#AlejoMaruriOnGmail14'


# Messages to user as pops
try:
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }
except Exception as e:
    pass


LOGIN_REDIRECT_URL = '/StudyCasesManage'
LOGOUT_REDIRECT_URL = '/StudyCasesManage'
