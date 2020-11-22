from .settings import *

DEBUG = True
SECRET_KEY = "some secret"

INSTALLED_APPS += ['debug_toolbar']

DATABASES['default'].update({
    'NAME': 'mdb',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'PORT': '3306',
})

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': 5,
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, '../media_root')

INSTALLED_IPS = [
    '127.0.0.1'
]