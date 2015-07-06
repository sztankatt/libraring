"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
"""PROJECT INFO"""
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'usr.project.project_info',
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = ['www.libraring.co.uk',
                 'libraring.co.uk']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5p0alevq3pcg)=$32k&yl907q+n%0m(tekvj+xigp55a-zd@z^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

LOGIN_REDIRECT_URL = '/usr/'

LOGIN_URL = '/usr/login/'

LOGOUT_URL = '/usr/logout/'

THUMBNAIL_DEBUG = DEBUG

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

INSTALLED_APPS = (
    #django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #3rd party apps
    'fontawesome',
    'haystack',
    'django_select2',
    'sorl.thumbnail',
    'widget_tweaks',
    'easy_pjax',
    'django_countries',
    
    #my apps
    'usr',
    'ajax',
    'books',
    'manager',
)

MIDDLEWARE_CLASSES = (   
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'libraring_db',
        'USER':'libraring_db_usr',
        'PASSWORD':'qHd258sLt1w',
    }
}

#emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.webfaction.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'admins'

EMAIL_HOST_PASSWORD = 'njdjdyAsd31415'

EMAIL_USE_TLS = True

WHOOSH_INDEX = os.path.join(os.path.dirname(BASE_DIR), "whoosh")

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    MEDIA_URL = '/media/'
    STATIC_ROOT = '/home/libraring/webapps/libraring_static/'
    MEDIA_ROOT = '/home/libraring/webapps/libraring_static/media/'
    
    STATICFILES_DIRS = (
        '/home/libraring/webapps/libraring/static/',
    )
    
    TEMPLATE_DIRS = (
        '/home/libraring/webapps/libraring_static/templates/',
    )
