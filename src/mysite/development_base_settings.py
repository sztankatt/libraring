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

ALLOWED_HOSTS = []

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5p0alevq3pcg)=$32k&yl907q+n%0m(tekvj+xigp55a-zd@z^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

THUMBNAIL_DEBUG = DEBUG

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'

TEMPLATE_DEBUG = DEBUG

LOGIN_REDIRECT_URL = '/usr/'

LOGIN_URL = '/usr/login/'

LOGOUT_URL = '/usr/logout/'


#emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.webfaction.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'admins'

EMAIL_HOST_PASSWORD = 'njdjdyAsd31415'

EMAIL_USE_TLS = True

# Application definition


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
    'debug_toolbar',
    'haystack',
    'django_select2',
    'sorl.thumbnail',
    'widget_tweaks',
    'easy_pjax',
    'django_countries',
    'endless_pagination',

    #my apps
    'usr',
    'ajax',
    'books',
)


WHOOSH_INDEX = os.path.join(os.path.dirname(BASE_DIR), "whoosh")

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'queued_search.signals.QueuedSignalProcessor'

QUEUE_BACKEND = 'sqs'
AWS_ACCESS_KEY_ID = 'AKIAILBR5EVBRKC2MOCA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'eu-west-1'
SEARCH_QUEUE_NAME = 'libraring_books_local'

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
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': 'mydatabase',
    #},
    #
	#MYSQL default
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'libraring',
        'USER':'root',
        'PASSWORD':'123',
        'HOST':'localhost',
        'PORT':'3306',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('hu', 'Hungarian'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "templates"),
)

if DEBUG:
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static-only")
    
    STATICFILES_DIRS = (
        os.path.join(os.path.dirname(BASE_DIR), "static"),
    )
        
    MEDIA_URL = '/media/'
    
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
