from pathlib import Path
import environ
import os
# import django_heroku
from django.contrib import messages


# Initialise environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')
# SECRET_KEY = 'e^3_1uf=ap%88vq0__j^c^3t1ytx^t4t-)398nu^@#l5v-d4&0'

ALLOWED_HOSTS = ['127.0.0.1', 'https://saveensexpenseapp.herokuapp.com/']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expensesapp',
    'authentication',
    'userpreferences',
    'incomeapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'expenseswebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'expenseswebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_USER_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }

    STATIC_URL = 'static/'
    STATICFILES_DIRS=[
        BASE_DIR / 'expenseswebsite/static'
    ]
    STATIC_ROOT = BASE_DIR / 'staticfiles'

else: #for production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('dbname'),
            'USER': env('user'),
            'PASSWORD': env('password'),
            'HOST': env('host'),
            'PORT': env('port'),
        }
    }

    # for vercel
    STATIC_URL = 'static/'
    STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'
# # STATICFILES_DIRS=[
# #     BASE_DIR / 'expenseswebsite/static'
# # ]
# # STATIC_ROOT = BASE_DIR / 'staticfiles'
#
# #for vercel
# STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
#

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

#email stuff
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# django_heroku.settings(locals())
