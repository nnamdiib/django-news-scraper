import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# I am using a PostgreSQL DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news',
        'USER': 'nnamdi',
        'PASSWORD': os.environ.get('NEWS_APP_DB_PASS'),
        'HOST': 'localhost',
        'PORT': '',
    }
}