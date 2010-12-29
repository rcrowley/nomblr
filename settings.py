import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Richard Crowley', 'r@rcrowley.org'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nomblr',
        'OPTIONS': {
            'init_command': 'SET storage_engine = InnoDB',
        },
        'USER': 'root',
    }
}

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-US'
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin/media/'

SECRET_KEY = '7)u3-xsj6ud(8(k_sc=6n48c0tqs#b_@_v6$o&df9hxl&(1hgt'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'nomblr.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_nose',
    'gunicorn',
    'haystack',
    'nomblr',
    'nomblr.account',
    'nomblr.recipes',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

USERNAME_BLACKLIST = (
    'account',
    'admin',
    'api',
    'blog',
    'friends',
    'help',
    'invite',
    'login',
    'logout',
    'me',
    'mine',
    'settings',
    'signup',
    'you',
)

HAYSTACK_ITERATOR_LOAD_PER_QUERY = 15
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15
HAYSTACK_SITECONF = 'nomblr.search_site'
HAYSTACK_SOLR_URL = 'http://localhost:9000/solr'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEFAULT_FROM_EMAIL = 'Nomblr <noreply@nomblr.com>'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PROFILE_MODULE = 'account.Profile'
