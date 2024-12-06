"""
Django settings for IRCTC_Backend_API project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os
from datetime import timedelta
# Fetch DATABASE_URL and normalize the scheme
raw_database_url = os.environ.get('DATABASE_URL', '')
normalized_database_url = raw_database_url.replace('postgresql://', 'postgres://')




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y4_5&#rj@3v8)#2d$!ycio8400@c!k55(ut4o3d6x9_tk2_tu2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booking.apps.ApiConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'IRCTC_Backend_API.urls'

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

WSGI_APPLICATION = 'IRCTC_Backend_API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    
# }
#DATABASE_URL = "postgresql://users_wo3t_user:RlvE7gRJ81jHC7EsYM6acO6vd2Uu5sP7@dpg-ct91lv3v2p9s73eoqcl0-a.singapore-postgres.render.com/users_wo3t"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'users_wo3t',
        'USER': 'users_wo3t_user',
        'PASSWORD': 'RlvE7gRJ81jHC7EsYM6acO6vd2Uu5sP7',
        'HOST': 'dpg-ct91lv3v2p9s73eoqcl0-a.singapore-postgres.render.com',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
#os.environ['DATABASE_URL'] = 'postgresql://users_wo3t_user:RlvE7gRJ81jHC7EsYM6acO6vd2Uu5sP7@dpg-ct91lv3v2p9s73eoqcl0-a.singapore-postgres.render.com/users_wo3t '


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
