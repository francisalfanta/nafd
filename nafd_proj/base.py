INSTALLED_APPS = (
    # common apps...
)

# Django settings for mysite project.
import os

ALLOWED_HOSTS = ['localhost',]
SITE_ROOT   = os.path.dirname(os.path.realpath(__file__))

ADMINS = (
    ('Francis T. M. Alfanta', 'francisalfanta@gmail.com'),
)

MANAGERS = ADMINS
'''

    'default': {
        'ENGINE':   'django.db.backends.oracle',  #'django.db.backends.postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     'xe',                         # 'postgres'Or path to database file if using sqlite3.
        'USER':     'ccad',                       # 'ccad',       #  postgres'    Not used with sqlite3.
        'PASSWORD': 'ccad',                       # 'ccad',       #  admin'       Not used with sqlite3.
        'HOST':     'localhost',                  # 'localhost'Set to empty string for localhost. Not used with sqlite3. 
        'PORT':     '1521',                       # '5432'Set to empty string for default. Not used with sqlite3.
    }
'''
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',   # Add 'django.db.backends.oracle', 'django.db.backends.postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     'ccad',                       # 'xe',         # 'postgres'Or path to database file if using sqlite3.
        'USER':     'ccad',                       # 'ccad',       #  postgres'    Not used with sqlite3.
        'PASSWORD': 'ccad',                       # 'ccad',       #  admin'       Not used with sqlite3.
        'HOST':     '192.168.111.1',                  # 'localhost',  # 'localhost'Set to empty string for localhost. Not used with sqlite3. 
        'PORT':     '3306',                       # '1521',       # '5432'Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Manila'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

## Autocomplete
## added 07/16/2013
AUTOCOMPLETE_MEDIA_PREFIX = os.path.join(MEDIA_ROOT, 'autocomplete')

UPLOAD_PATH = 'attachments'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.    
    #"C:/Python27/Django-Projects/static", 
    "static", ## >>>> to be check 
    #os.path.join(SITE_ROOT, 'template/_images'),
    #os.path.join(SITE_ROOT, 'template/_static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@)42$0g10qks$2(m(3ekqlft=w_wwacmga6d822iz1u-wf@t=9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
     'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'ccad.NAFDUserMiddleware.NAFDUserMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (        
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'ccad.context_processors.nafd_staff',

)

ROOT_URLCONF = 'nafd_proj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'nafd_proj.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'template'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
### output settings ####

print 'MYSQL SITE ROOT: ', SITE_ROOT
print 'STATIC ROOT', STATIC_ROOT
print 'STATIC_URL', STATIC_URL

#AUTH_PROFILE_MODULE = 'ccad.UserProfile' # customize user model

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGINATE_BY': 10
}
# 01/16/2014
AUTH_USER_MODEL = 'ccad.NAFD_User'

#server = request.META.get('wsgi.file_wrapper', None)
#if server is not None and server.__module__ == 'django.core.servers.basehttp':
#    print 'inside dev'
import sys
RUNNING_DEVSERVER = (sys.argv[1] == 'runserver')
if RUNNING_DEVSERVER:
    print 'Running in Development mode'
else:
    print 'Running in Production mode'