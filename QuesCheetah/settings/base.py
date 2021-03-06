# Django settings for QuesCheetah project.

import os

# MySQL Database driver install
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    'corsheaders',

    # Project apps
    'main',
    'vote',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'QuesCheetah.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# uwsgi setting
WSGI_APPLICATION = 'QuesCheetah.wsgi.application'


"""
Database Settings
Check the CI document for the more information
about MySQL Database settings
"""

# Use the following live settings to build on Travis CI
if os.getenv('BUILD_ON_TRAVIS', None):
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'HOST': '127.0.0.1'
        }
    }

# Use the following live settings to build on circle CI
elif os.getenv('BUILD_ON_CRICLE', None):
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'circle_test',
            'USER': 'ubuntu',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'qc',
            'USER': 'root',
            'PASSWORD': 'audwn8593',
            'HOST': 'localhost',
            'PORT': ''
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'QuesCheetah', 'static'),
    ("node_modules", os.path.join(BASE_DIR, "node_modules")),
    ("jspm_packages", os.path.join(BASE_DIR, "jspm_packages")),
]

# CACHES = {
#     'default': {
#         'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

USE_ETAGS = True

# Set for LOGIN_URL
from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('main:user_login')
LOGOUT_URL = '/logout'

# Set Email option for alarm
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'asdf@gmail.com'
EMAIL_HOST_PASSWORD = "password"


# django-allauth library settings
AUTH_USER_MODEL = 'main.User'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

SOCIALACCOUNT_QUERY_EMAIL = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIALACCOUNT_PROVIDERS = {

    'facebook':
         {'METHOD': 'oauth2',
          'SCOPE': ['email'],
          'FIELDS': [
              'email',
              'name',
              'first_name',
              'last_name',
              'verified',
              'updated_time'],
          'VERIFIED_EMAIL': False,
          'VERSION': 'v2.4'},

    'google':
        {'SCOPE': ['profile', 'email', 'https://www.googleapis.com/auth/userinfo.email'],
             'AUTH_PARAMS': {
                 'access_type': 'online'
            }
        }
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = '/'

# django-cors-headers library settings
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
        'api-key',
        'jwt',
        'kid'
    )