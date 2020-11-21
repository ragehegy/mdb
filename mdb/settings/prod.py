from .default import *
import os
import django_heroku

# DEBUG = False

assert SECRET_KEY is not None,(
    'Please provide app SECRET_KEY env variable with a value.'
)

ALLOWED_HOSTS += [
    os.getenv('DJANGO_ALLOWED_HOSTS'), 
    'https://django-mdb.herokuapp.com/',
    'django-mdb.herokuapp.com',
    ]

# DATABASES['default'].update({
#     'NAME': os.getenv('DJANGO_DB_NAME'),
#     'USER': os.getenv('DJANGO_DB_USER'),
#     'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
#     'HOST': os.getenv('DJANGO_DB_HOST'),
#     'PORT': os.getenv('DJANGO_DB_PORT'),
# })
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            # 'sql_mode': 'traditional',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'NAME': 'django_mdb',
        'USER': 'o6gscqfi0dt6',
        'PASSWORD': '2~K5NTl%',
        'HOST': '160.153.133.177',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': int(os.getenv('DJANGO_CACHE_TIMEOUT')),
    }
}

# MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv("DJANGO_UPLOAD_S3_BUCKET")

django_heroku.settings(locals())