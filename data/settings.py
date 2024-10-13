import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'data_expenses.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'PASSWORD': ''
    },
}

#Since we only have one app which we use
INSTALLED_APPS = (
    'data',
)

SECRET_KEY = 'django-securefo-iwo4*4(puexb(y!b3+w!jyf_15i4tlpd&)wd9o)d-e52@5usf#'

USE_TZ = False
