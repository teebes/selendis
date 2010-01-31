import logging
import logging.handlers
import os

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SITE_FS_ROOT = os.path.realpath(os.path.abspath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '.')))

# loggers
LOGS_DIR = u"%s/logs" % SITE_FS_ROOT
if not hasattr(logging, 'setup_done'): # because django imports settings multiple times
    logging.setup_done = True
    
    # general logger
    stark_logger = logging.getLogger('StarkLogger')
    stark_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOGS_DIR + "/stark.log", maxBytes=1 * 1028 * 1028, backupCount=5)
    stark_logger.addHandler(handler)

    # logger specifically for the timing functions
    pulse_logger = logging.getLogger('PulseLogger')
    pulse_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOGS_DIR + "/pulses.log", maxBytes=1 * 1028 * 1028, backupCount=5)
    pulse_logger.addHandler(handler)

# Django settings for stark project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

""" add/remove hash mark to toggle DBs
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'stark'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
DATABASE_OPTIONS = {
    'sql_mode': 'TRADITIONAL,STRICT_ALL_TABLES,ANSI',
    'charset': 'utf8',
    'init_command': 'SET storage_engine=INNODB',
}
"""
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '%s/db' % SITE_FS_ROOT
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
#"""


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mo9#x^rs^skstw56!+oj$gq8fio6xp79(2!d^u(!4+8@o5kd#f'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'stark.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % SITE_FS_ROOT,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'stark.apps.accounts',
    'stark.apps.anima',
    'stark.apps.world',
    'stark.lib.uni_form',
    'piston',
)
