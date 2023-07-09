'''
Settings applied to the entire django project.

The current settings are for development and not suitable for production. Visit
https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/ for production settings.
'''


import os
import dj_database_url

from pathlib import Path


# BASE_DIR = django-locallibrary-tutorial/
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key is used by django to verify legitimacy of data (sessions, cookies, password reset request, etc.)
# received from user. Here, we are fetching from environment variable but using default value if not available.
# A secret key is automatically generated when you create a project, but you can create one using by running
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# Don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# This variable is for security purposes by restricting what host this application can serve.
# Typically, this is set to your domain (like example.com) in production and localhost for development.
# Railway is a platform for developers to build, run, and scale applications in the cloud.
ALLOWED_HOSTS = ['.railway.app','127.0.0.1']

# Similar to ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app','https://*.127.0.0.1']

# An app is a self-contained module that encapsulates a specific functionality of the larger web application
INSTALLED_APPS = [
    # Admin app
    'django.contrib.admin',
    # Core authentication framework and its default models
    'django.contrib.auth',
    # Django content type system (allows permissions to be associated with models)
    'django.contrib.contenttypes',
    # Enable sessions
    'django.contrib.sessions',
    # Stores simple, one-time notifications for the user between requests (like success of a form submission)
    'django.contrib.messages',
    # Manages static files
    'django.contrib.staticfiles',
    # Adds our new application
    'catalog.apps.CatalogConfig',
]

# Middleware processes requests and responses globally before they reach the view or the client.
# Used for session management, authentication, CSRF protection, etc.
MIDDLEWARE = [
    # Security enhancements like preventing cross-site scripting, clickjacking, etc.
    'django.middleware.security.SecurityMiddleware',
    # serving static files, making your project a self-contained without relying on nginx, Amazon S3, etc.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Enable sessions
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Helpful utils like appending trailing slashes, URL rewriting, setting content-length header, etc.
    'django.middleware.common.CommonMiddleware',
    # Protection against Cross-Site Request Forgeries
    'django.middleware.csrf.CsrfViewMiddleware',
    # Associates users with requests using sessions
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Enables cookie and session based messaging for one-time notifications between views
    'django.contrib.messages.middleware.MessageMiddleware',
    # Provides Clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Import path to your root url.py configs
ROOT_URLCONF = 'locallibrary.urls'

# Defines configurations for Django's template engines
TEMPLATES = [
    {
        # Template engine to use
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Tell Django where to look for html files
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # Django will also look for templates inside each of the INSTALLED_APPS
        'APP_DIRS': True,
        'OPTIONS': {
            # functions that Django's template engine uses to mix some variables into the context of your templates
            'context_processors': [
                # Adds a variable DEBUG to the context, representing whether Debug mode is active
                'django.template.context_processors.debug',
                # Adds a variable request to the context, representing the current HttpRequest
                'django.template.context_processors.request',
                # Adds several variables to the context, most importantly user
                'django.contrib.auth.context_processors.auth',
                # Adds a variable messages to the context, which represents messages for the user
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Path of the WSGI application object that Django will use
WSGI_APPLICATION = 'locallibrary.wsgi.application'


# Database information. More configs needed to be provided to use postgres SQL on Amazon RDS
# (https://docs.djangoproject.com/en/4.0/ref/settings/#databases)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Update database configuration from $DATABASE_URL environment variable (if defined)
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#  List of validators that are used to check the strength of user's passwords.
# (https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators)
AUTH_PASSWORD_VALIDATORS = [
    {
        # Checks the similarity between the password and a set of attributes of the user.
        # For example, if password is similar to email address, reject the password.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Checks whether the password has a minimum number of characters
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Compares the password against a list of the 20,000 most common passwords
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Checks if the password is entirely numeric (i.e., whether the password is a number)
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Language to use for this installation (translate debug message from debug etc.)
# ( https://docs.djangoproject.com/en/4.0/topics/i18n/)
LANGUAGE_CODE = 'en-us'

# Time zone that Django will use to handle date and time representations
TIME_ZONE = 'UTC'

# Determines if Django's internationalization system should be enabled.
# This provides hooks for translation of text in models, views, and templates. You still need to do
# the actual translation work
USE_I18N = True

# Determines if Django will use timezone-aware datetimes
USE_TZ = True

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# Enables content sent via email to be sent via console for debugging.
# Email structure needs to be configured otherwise.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files (CSS, JavaScript, Images) (https://docs.djangoproject.com/en/4.0/howto/static-files/)
# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'

# Static file serving.
# (http://whitenoise.evans.io/en/stable/django.html#django-middleware)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Define the type of auto-created primary key fields when you don't declare them explicitly in your models.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
