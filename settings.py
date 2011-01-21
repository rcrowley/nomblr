import os
import os.path

DEBUG = 'NOMBLR_VIA' not in os.environ
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Richard Crowley', 'r@rcrowley.org'),
)
MANAGERS = ADMINS

if 'Darwin' == os.uname()[0]:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'nomblr.db',
        }
    }
else:
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
    'nomblr.follows',
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

RECIPE_BLACKLIST = (
    'follow',
    'friends',
    'unfollow',
)

HAYSTACK_SITECONF = 'nomblr.search_site'
if 'Darwin' == os.uname()[0]:
    HAYSTACK_SEARCH_ENGINE = 'whoosh'
    HAYSTACK_WHOOSH_PATH = 'nomblr.index'
else:
    HAYSTACK_SEARCH_ENGINE = 'solr'
    HAYSTACK_SOLR_URL = 'http://localhost:9000/solr'
HAYSTACK_ITERATOR_LOAD_PER_QUERY = 15
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEFAULT_FROM_EMAIL = 'Nomblr <noreply@nomblr.com>'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nomblr@rcrowley.org'
EMAIL_HOST_PASSWORD = 'Nie6pooX'
EMAIL_USE_TLS = True

AUTH_PROFILE_MODULE = 'account.Profile'

# for N in $(seq 10); do dd if=/dev/urandom bs=1024 count=1 2>/dev/null | sha1sum | cut -d" " -f1 | xargs -I__ echo "    '__',"; done
INVITE_CODES = (
    'aa073e50954855d0533476ad002cce721d1b830d', # Richard
    '40d34e87b489abb396d4b6a4a76858bb26b44582', # Cap
    '193fc93fae56728443ecae4c0746feb70c0d1d14',
    'c774838bb1d410c00df127f02b389d86ad6c2bc8',
    'f49a92b37661eef7650d68155c93f4e117c3e4e1',
    '1a92be8a1433a722ab68c4008b335a8df7474ca0',
    '6b0471a0ed8331a14377090d6092e2850256f82e',
    'e9d65034adbe521db55a4b6f4c8f7842a5a849f2',
    '1cadb092a5eeee385f6823096c40e7af616ed1f4',
    'c0723bf9bd1df69d25151fc23a0918dd304ef1d3',
)
