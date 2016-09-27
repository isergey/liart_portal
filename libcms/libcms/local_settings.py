# Django settings for libcms project.
from settings import PROJECT_PATH
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# site domain name
SITE_DOMAIN = 'liart.ru'
ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Sergey', 'dostovalov@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'artlib',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '123456',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        }
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60,
        }
}

#TEMPLATE_LOADERS = (
#    (
#        'django.template.loaders.cached.Loader', (
#            'django.template.loaders.filesystem.Loader',
#            'django.template.loaders.app_directories.Loader',
#        )),
#        'django.template.loaders.eggs.Loader',
#    )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_PATH + '../var/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_PATH + '../var/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_PATH + 'static_init/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(1gg70@rp5gken-x#stkj#$(y9b(2q#c!w%l1u@75dq&amp;d8r#+e'

EMAIL_HOST = 'smtp.liart.ru'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'cio'
EMAIL_HOST_PASSWORD = '56AfkVjl'
#DEFAULT_FROM_EMAIL = 'system@liart.ru'
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@liart.ru'
EMAIL_HOST_PASSWORD = '7bdb01a74efd2045bf5e527c820b497c'
EMAIL_USE_TLS = False

FILEBROWSER = {
    'upload_dir': MEDIA_ROOT + 'files/',
    'upload_dir_url': MEDIA_URL + 'files/'
}

ASK_LIBRARIAN = {
    'MAIN_DISPATCHER': 'cio@liart.ru'
}