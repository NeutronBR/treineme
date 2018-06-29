"""
Django settings for treineme project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '0!3)pykibt!uld)qi@nx1uu8#+h^nq3vqcmvm&_r4nb+3z4=me'
# SECRET_KEY = os.getenv('SECRET_KEY', 'Valor padrão opcional')
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['mighty-castle-93813.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'whitenoise.runserver_nostatic',
    'widget_tweaks',
    'taggit',
    'storages',

    'usuarios',
    'cursos',
    # 'cursos.apps.CursosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'urls'

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

                'context_processors.nome_empresa',
                'context_processors.treineme_site',
            ],
        },
    },
]

WSGI_APPLICATION = 'treineme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
#
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'banco',
        # 'USER': 'user',
        # 'PASSWORD': 'senha',
        # 'HOST': '',
        # 'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
#     os.path.join(PROJECT_ROOT, 'static'),
# )

MEDIA_ROOT = os.path.join(BASE_DIR, 'treineme', 'media')
MEDIA_URL = '/media/'

# Auth
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'usuarios:painel'
LOGOUT_URL = 'usuarios:logout'


# Nome da empresa pela aplicação
NOME_EMPRESA = 'PUC-MG'
TREINEME_SITE = os.getenv('TREINEME_SITE')


# E-mails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL')
DEFAULT_FROM_EMAIL = '{} Treine-ME <{}> '.format(NOME_EMPRESA, CONTACT_EMAIL)


# Change 'default' database configuration with $DATABASE_URL.
# import dj_database_url
db = dj_database_url.config(conn_max_age=600)
# db = dj_database_url.config(conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db)
# DATABASES['default'].['CONN_MAX_AGE'] = 500

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TAGGIT_CASE_INSENSITIVE = True


# set S3 as the place to store your files.
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_QUERYSTRING_AUTH = False  # This will make sure that the file URL does not have unnecessary parameters like your access key.
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com'
AWS_LOCATION = '/media/'  # estrutura do bucket tem o /media/ sem essa config, não consegue encontrar o path
MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/'



try:

    from django.contrib.messages import constants as messages

    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger'
    }

    from local_settings import *

except ImportError as e:
    print(e)



# Video.objects.filter(aula__in=Aula.objects.filter(curso=curso))
# Aula.objects.filter(curso__inscricao__usuario='Bruno')
