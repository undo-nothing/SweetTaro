import os
import sys
import configparser
from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%n=qka!hlj28jiq1%z+!+)=m16a&g=l2g%_8=apx_2*%*(rbc('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CONFIG_FILE = configparser.RawConfigParser(strict=False, allow_no_value=True)
if DEBUG:
    CONFIG_FILE.read(os.path.join(BASE_DIR, 'config-dev.ini'))
else:
    CONFIG_FILE.read(os.path.join(BASE_DIR, 'config-prod.ini'))

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'accounts.User'
AUTH_PROFILE_MODULE = 'accounts.UserProfile'


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    'apps.accounts',
    'apps.bing_wapper',
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
if CONFIG_FILE.getboolean('SYSTEM', 'CSRF_ALLOW', fallback='False'):
    MIDDLEWARE.append('apps.api.middleware.CsrfMiddleware')

ROOT_URLCONF = 'SweetTaro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'SweetTaro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': CONFIG_FILE.get('DATABASE', 'NAME'),
        'ENGINE': 'django.db.backends.%s' % CONFIG_FILE.get('DATABASE', 'ENGINE'),
        'USER': CONFIG_FILE.get('DATABASE', 'USER'),
        'PASSWORD': CONFIG_FILE.get('DATABASE', 'PASSWORD'),
        'HOST': CONFIG_FILE.get('DATABASE', 'HOST'),
        'PORT': CONFIG_FILE.get('DATABASE', 'PORT'),
        'CONN_MAX_AGE': 0,
        'AUTOCOMMIT': True,
        'DISABLE_SERVER_SIDE_CURSORS': True
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# django-rest-framework setting
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 分页配置选项
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    # 配置过滤
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    # 文档
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}


REDIS_HOST = CONFIG_FILE.get('REDIS', 'REDIS_HOST')
REDIS_PORT = CONFIG_FILE.getint('REDIS', 'REDIS_PORT')
REDIS_PASSWORD = CONFIG_FILE.get('REDIS', 'REDIS_PASSWORD')
CACHE_REDIS_DB = CONFIG_FILE.getint('CACHE', 'CACHE_REDIS_DB')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://:%s@%s:%s/%s' % (REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, CACHE_REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        'TIMEOUT': 7 * 24 * 60 * 60

    }
}
