"""
Django settings for pl_sandbox project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, docker, logging

from pl_sandbox.testing import DatabaselessTestRunner

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+61drt2^c32qp)knvy32m*xm*ew=po%f8a9l!bp$kd7mz3(109'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'sandbox',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = []

ROOT_URLCONF = 'pl_sandbox.urls'

WSGI_APPLICATION = 'pl_sandbox.wsgi.application'


# Database
DATABASES = {}

# Needed for manage.py to run without database
TEST_RUNNER = 'pl_sandbox.testing.DatabaselessTestRunner'

# Password validation
AUTH_PASSWORD_VALIDATORS = []

#Write email in console instead of sending it if DEBUG is set to True
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Logger information
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)-15s] %(levelname)s -- File: %(pathname)s line n°%(lineno)d -- %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(asctime)-15s] %(levelname)s -- %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local6',
            'address': '/dev/log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '':{
            'handlers': ['console', 'syslog', 'mail_admins'],
            'level': 'INFO',
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'tmp')
MEDIA_URL = '/tmp/'


# Sandbox parameters
# DEL_ENV_AFTER: number of days before a normal environment should be deleted
# DEL_TEST_ENV_AFTER: number of days before a test environment should be deleted
SANDBOX_VERSION = "1.0.0"
DEL_ENV_AFTER = 12*30
DEL_TEST_ENV_AFTER = 7


# Docker parameters
DOCKER_IMAGE = "pl:base"
DOCKER_ENV_VAR = {}   #(dic) Environment variables to set inside the container, as a dictionary.
DOCKER_MEM_LIMIT = "10m"  #(str) Memory limit. String with a units identification char (13b, 12k, 14m, 1g) min is 4m.
DOCKER_MEMSWAP_LIMIT = 0  #(str) See https://docs.docker.com/engine/admin/resource_constraints/#--memory-swap-details
DOCKER_CPUSET_CPUS = "0"  #(str) CPUs in which to allow execution ("0-3", "0,1").

try:
    from pl_sandbox.config import *
except:
    logger = logging.getLogger(__name__)
    logger.exception("No config file found.")
    pass

 # Docker creating function
def CREATE_DOCKER():
    return docker.from_env().containers.run(
        DOCKER_IMAGE,
        detach=True,
        environment=DOCKER_ENV_VAR,
        auto_remove=True,
        tty=True,
        cpuset_cpus=DOCKER_CPUSET_CPUS,
        mem_limit=DOCKER_MEM_LIMIT,
        memswap_limit=DOCKER_MEMSWAP_LIMIT
    )
